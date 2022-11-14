import json
import boto3
from datetime import datetime, timezone, timedelta


today = datetime.now(timezone.utc)

s3 = boto3.client('s3', region_name='us-east-1')


def lambda_handler(event, context):
    print(event)
    bucket = event.get('bucket', None)
    
    if not bucket:
        print(f'bucket key value not found in the event. {event}')
        return
    
    objects = s3.list_objects(Bucket=bucket)
    
    print(today + timedelta(days=-2))
    for o in objects["Contents"]:
        if o["LastModified"] <= today  + timedelta(days=-1):
            print(o["Key"],  o["LastModified"])
            response = s3.delete_object(Bucket=bucket, Key=o["Key"])
            print(f'Deleted the file ({o["Key"]}) with response - {response}')
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
