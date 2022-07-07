import boto3
import os


def download_dir(client, resource, dist, local='/tmp', bucket='your_bucket'):
  
    paginator = client.get_paginator('list_objects')
    
    for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dist):
      
        if result.get('CommonPrefixes') is not None:
            for subdir in result.get('CommonPrefixes'):
                download_dir(client, resource, subdir.get('Prefix'), local, bucket)
                
        for file in result.get('Contents', []):
            dest_pathname = os.path.join(local, file.get('Key'))
            
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
              
            if not file.get('Key').endswith('/'):
                resource.meta.client.download_file(bucket, file.get('Key'), dest_pathname)


client = boto3.client('s3')
resource = boto3.resource('s3')

download_dir(client, resource,
             'Glue-Job-Scripts/',
             r'C:\Users\vpandian\tmp',
             bucket='arod-artefacts')
