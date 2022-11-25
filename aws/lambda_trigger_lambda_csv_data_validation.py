"""
  Triggered on the Cloud event and performs the data validation.
"""
import boto3
import os
import logging
import codecs
import pandas as pd
import json

#####################################################
#  VARIABLES
#####################################################


file_name = os.path.splitext(os.path.basename(__file__))[0]

default_log_args = {
    "level": logging.DEBUG if os.environ.get("DEBUG", 0) else logging.INFO,
    "format": "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    "datefmt": "%d-%b-%y %H:%M"
}

root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)

sample_records = 100
data_records = []
data_column = []
with_header = True
data_validation_flag = True
global row_count, column_count, comment
row_count =0
column_count = 0
comment = []

file_formats = ['.txt', '.csv', '.tsv']
file_names = ['prof']  # , 'inst', 'rx'
template = { 
    'prof': { 79: 'prof_v3_template.csv', 74: 'prof_v2_template.csv'}
}

#####################################################
#  FUNCTIONS
#####################################################


def get_logger(name):
    logging.basicConfig(**default_log_args)
    return logging.getLogger(name)


def get_split_char(key):
    if key.lower().endswith('.tsv'):
        return '\t'
    elif key.lower().endswith('.csv'):
        return ','
    elif key.lower().endswith('.txt'):
        return '|'
    else:
        return ' '


def get_row_count_of_s3_csv(bucket_name, path):
    req = boto3.client('s3').select_object_content(
        Bucket=bucket_name,
        Key=path,
        ExpressionType="SQL",
        Expression="""SELECT count(*) FROM s3object """,
        InputSerialization={"CSV": {"FileHeaderInfo": "Use",
                                    "AllowQuotedRecordDelimiter": True}},
        OutputSerialization={"CSV": {}},
    )
    row_count = next(int(x["Records"]["Payload"]) for x in req["Payload"])
    return row_count
    


#####################################################
#  MAIN LAMBDA EVENT
#####################################################


def lambda_main(event: dict = None, context: dict = None):
    try: 
        global row_count, column_count
        log = get_logger(f"{file_name}.{lambda_main.__name__}")
        log.info('=' * 30 + " Init " + '=' * 30)
        log.info(f"[*] event - {event}")
        log.info(f"[*] context - {context}")
        records = event.get("Records", None)
        
        if not records:
            log.info(f"[-] No Records found in the events - {event}")
            return None
    
        new_file = [{'bucket': record["s3"]["bucket"]["name"],
                      'key': record['s3']['object']['key'],
                      'size': record['s3']['object']['size']}
                     for record in records
                     if record.get("s3")]
                     
        new_file = new_file[0]
        s3 = boto3.resource("s3")
        key = new_file['key']
        bucket = new_file['bucket']
        
        
        if any(key.lower().endswith(fmt) for fmt in file_formats):
            msg = '>>>>>>> [+] Expected File Format matched'
            comment.append(msg)
            log.info(msg)
        else:
             msg = '>>>>>>> [-] Expected File Format unmatched'
             comment.append(msg)
             log.info(msg)
             return -1
        
        if any(fmt in key.lower() for fmt in file_names):
            msg  = '>>>>>>> [+] Expected File Name matched'
            comment.append(msg)
            log.info(msg)
        else:
             msg = '>>>>>>> [-] Expected File Name unmatched'
             comment.append(msg)
             log.info(msg)
             return -1
        
        
        row_count = get_row_count_of_s3_csv(bucket, key)
        log.info(f'>>>>>>> [+] Row_Count = {row_count}')
        split_char = get_split_char(key)
        idx = 0
        s3_object = s3.Object(new_file['bucket'], key)
        line_stream = codecs.getreader("utf-8")
        for line in line_stream(s3_object.get()['Body']):
            # log.info(f"line is {line}")
            if idx == 0:
                data_column = [value.strip() for value in line.split(split_char)]
            else:
                data_records.append([value.strip() for value in line.split(split_char)])
            idx += 1
            if idx > sample_records:
                break
          
        log.info(f'>>>>>>> [+] Collected Sample records = {sample_records}') 
        log.info(f'>>>>>>> Column Length - {len(data_column)}')
        
        # Check Sample Records has headers 
        template_file = ''
        if 'prof' in key.lower():
            template_file = template['prof'].get(len(data_column), '')
        
        if not template_file:
            log.info('>>>>>>> [-] Template File not found.')
            return -1
        
        log.info(f'>>>>>>> [+] Template File found - {template_file}')
        csv_df = pd.read_csv(open(template_file))
        # print(csv_df.columns)
        # print(csv_df.head())
        # print(csv_df[['Seq', 'ColumnName']].values.tolist())
        # print('|'.join(csv_df['ColumnName'].values.tolist()))
        expected_columns = csv_df['ColumnName'].values.tolist()
        actual_columns = data_column
        log.info(f'=====>> {len(expected_columns)} == {len(actual_columns)}')
        log.info(f'=====>> {set(expected_columns) - set(actual_columns)}/{set(actual_columns) - set(expected_columns)}')
        log.info(f'=====>> type(data_records) = {type(data_records)}{len(data_records)} type(data_column)  = {type(data_column)}{len(data_column)}')
      
        if expected_columns == actual_columns:
            log.info('>>>>>>> [+] Header found.')
            df = pd.DataFrame(data=data_records, columns=data_column)
        else:
            log.info('>>>>>>> [-] Header is not found.')
            df = pd.DataFrame(data=data_records.append(data_column), columns=expected_columns)
    
        print(df.head())
        # print(df.describe())
        # print(df.columns)
        actual_columns = list(df.columns)
        
        # dataframe.size
        size = df.size
        # dataframe.shape
        shape = df.shape
        # printing size and shape
        log.info(">>>>> Size = {} | Shape ={} | Shape[0] x Shape[1] = {}".format(size, shape, shape[0]*shape[1]))
        column_count = shape[1]
        log.info(f'>>>>>>> Column_Count = {column_count}')
        
        if len(expected_columns) == column_count:
            msg = '[+] Column Count Matched'
            comment.append(msg)
            log.info(msg)
        else:
            msg = '[-] Column Count Unmatched'
            comment.append(msg)
            log.info(msg)
            return -1
        
        if expected_columns == actual_columns:
            msg  = '[+] Column Order & Name Matched'
            comment.append(msg)
            log.info(msg)
        else:
            msg = '[-] Column Order & Name Unmatched'
            comment.append(msg)
            log.info(msg)
            return -1
        if template_file == 'prof_v3_template.csv':
            log.info(f" >>> df['Member Sex'].isin(['M', 'F', 'U'] = {all(df['Member Sex'].isin(['M', 'F', 'U']).tolist())}")
            for col in ['Claim Paid Date', 'Payment Adjudication Date', 'Claim Submission Date', 'Member Date of Birth (DOB)', 'Member Date of Death (DOD)', 'Beginning Date of Service', 'Ending Date of Service']:
                m1 = df[col].eq('') | df[col].isna()
                m2 = pd.to_datetime(df[col], format='%m/%d/%Y', errors='coerce').isna()
                log.info(f">>>> Date Validation - {col} = {m1.eq(m2).all()}")
            return 1 
    except Exception as err:
        comment.append(sr(err))
        return -1


def lambda_handler(event: dict = None, context: dict = None):
      
    log = get_logger(f"{file_name}.{lambda_handler.__name__}")
    if lambda_main(event, context):
        kwargs = {"row_count": row_count,
            "column_count": column_count,
            "data_validation_flag": True, 
            "comment":  '|'.join(comment)}
    else:
        log.info('Data validation failed')
        kwargs = {"row_count": row_count,
            "column_count": column_count,
            "data_validation_flag": False, 
            "comment":  '|'.join(comment)}
    log.info(f'{kwargs}')
    
    _records  = event['Records'][0]
    _records['row_count'] = kwargs['row_count']
    _records['column_count'] = kwargs['column_count']
    _records['data_validation_flag'] = kwargs['data_validation_flag']
    _records['comment'] =  kwargs['comment']
    
    lambda_client = boto3.client('lambda')
 
    lambda_client.invoke(FunctionName='File-Meta-Data-Catcher', 
                         InvocationType='Event',
                         Payload=json.dumps(event))
    log.info('=' * 30 + " Exit " + '=' * 30)
    
