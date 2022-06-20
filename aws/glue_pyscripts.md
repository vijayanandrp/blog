## Glue trigger

```python
glue = boto3.client('glue')
glue.start_crawler(Name='test_crawler')
logger.info('Starting the glue jobs')
arguments = {
    '--SOURCE': 'source',
    '--REPORT': 'report',
    '--DATE': 'date',
    '--BUCKET': 'new_file',
    '--KEY': 'new_file',
    '--SIZE': 'size',
}
logger.info(f'arguments - {arguments}')

response = glue.start_job_run(
    JobName='insights_glue',
    Arguments=arguments,
    Timeout=2660,
    NotificationProperty={})
logger.info(f"[*] JobRunId - {response['JobRunId']}")
logger.info(f"[*] response - {response}")
```


## Monitor Glue Jobs

https://stackoverflow.com/questions/56370794/aws-glue-python-shell-job-can-call-aws-glue-spark-job

```python
import boto3
client = boto3.client(service_name='glue', region_name='us-east-1',
          endpoint_url='https://glue.us-east-1.amazonaws.com') 
response = client.start_job_run(JobName='WHICH U CREATED IN CONSOLE')
status = client.get_job_run(JobName=job_name, RunId=response['JobRunId'])

if status:
    state = status['JobRun']['JobRunState']
    while state not in ['SUCCEEDED']:
        time.sleep(30)
        status = client.get_job_run(JobName=job_name, RunId=response['JobRunId'])
        state = status['JobRun']['JobRunState']
        if state in ['STOPPED', 'FAILED', 'TIMEOUT']:
            raise Exception('Failed to execute glue job: ' + status['JobRun']['ErrorMessage'] + '. State is : ' + state)
            
 ```
 
 ## Get Glue or Python Shell Job ID
 
 ```python
 def get_running_job_id(job_name):
    session = boto3.session.Session()
    glue_client = session.client('glue')
    try:
        response = glue_client.get_job_runs(JobName=job_name)
        for res in response['JobRuns']:
            print("Job Run id is:"+res.get("Id"))
            print("status is:"+res.get("JobRunState"))
            if res.get("JobRunState") == "RUNNING":
                return res.get("Id")
        else:
            return None
    except ClientError as e:
        raise Exception("boto3 client error in get_status_of_job_all_runs: " + e.__str__())
    except Exception as e:
        raise Exception("Unexpected error in get_status_of_job_all_runs: " + e.__str__())
```
 
 X
 ```python
 import sys
from awsglue.utils import getResolvedOptions

args = getResolvedOptions(sys.argv, [])
job_run_id = args['JOB_RUN_ID']
```

```
./bin/gluesparksubmit path/to/job.py --JOB_NAME=my-job --input_file_path='s3://path'
```

```python
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'input_file_path'])
print(args['JOB_NAME'])
print(args['input_file_path'])
```




