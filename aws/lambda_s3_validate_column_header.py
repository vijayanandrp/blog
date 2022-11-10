import boto3
import os
import logging
import codecs


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


def get_logger(name):
    logging.basicConfig(**default_log_args)
    return logging.getLogger(name)

def compare_dict(x, y):
    print(y)
    shared_items = {k: x[k] for k in x if k in y and x[k] == y[k]}
    if len(shared_items) == len(x) == len(y):
        return True
    else:
        return False


templates = [{1: 'User name', 2: 'Password', 3: 'Access key ID', 4: 'Secret access key', 5: 'Console login link'}, {1: 'sha1'}]

def lambda_handler(event: dict = None, context: dict = None):
    log = get_logger(f"{file_name}.{lambda_handler.__name__}")
    log.info('=' * 30 + " Init " + '=' * 30)
    log.info(f"event - {event}")
    log.info(f"context - {context}")
    records = event.get("Records", None)
    if not records:
        log.info(f"[-] No Records found in the events - {event}")
        return None

    new_files = [{'bucket': record["s3"]["bucket"]["name"],
                  'key': record['s3']['object']['key'],  # m5/insights/new_user_report/date=2022-05-22
                  'size': record['s3']['object']['size']}
                 for record in records
                 if record.get("s3")]

    glue = boto3.client('glue')
    log.info('Starting the glue jobs')
    for new_file in new_files:
        log.info(f'>>>>> New File - {new_file}')
        key = new_file['key']
        s3 = boto3.resource("s3")
        s3_object = s3.Object(new_file['bucket'],key )
        line_stream = codecs.getreader("utf-8")
        
        split_char = '|'
        if key.lower().endswith('.tsv'):
            split_char = '\t'
        elif key.lower().endswith('.csv'):
            split_char = ','
        elif  key.lower().endswith('.txt'):
            spit_char = '|'
            
        
        idx = 0
        headers = None
        for line in line_stream(s3_object.get()['Body']):
            print(line)
            if line.strip():
                headers = [(idx+1, l.strip()) for idx, l in  enumerate(line.split(split_char))]
                break
        
        x = dict(headers)
        for y in templates:
            if compare_dict(x, y):
                log.info(f'[+] Template Match found - {x}')
            else:
                log.info(f'[+] Template Match Failed - {x}')
    log.info('=' * 30 + " Exit " + '=' * 30)
    return
