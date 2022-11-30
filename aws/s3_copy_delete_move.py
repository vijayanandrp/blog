    # COPY tar.gz, .tsv and .fin files to archive directory
    logger.info(f' >>>>> Moving S3 files ')
    BUCKET = source_bucket
    INPUT_PATH = f'{source_key}'
    OUTPUT_PATH = f'{dest_key}'
    s3_client = boto3.client('s3')
    # Create a reusable Paginator
    paginator = s3_client.get_paginator('list_objects_v2')
    # Create a PageIterator from the Paginator
    page_iterator = paginator.paginate(Bucket=BUCKET, Prefix=INPUT_PATH)
    # Loop through each object, looking for ones older than a given time period
    for page in page_iterator:
        if 'Contents' in page:
            for object in page['Contents']:
                # if object['LastModified'] < dt.now().astimezone() - timedelta(hours=1):  # <-- Change time period here
                # Strip off input path and add output path
                source_key = object['Key']
                if not any(source_key.lower().endswith(x) for x in ['.tsv', '.tar.gz', '.fin']):
                    continue
                target_key = OUTPUT_PATH + source_key[len(INPUT_PATH):]
                logger.info(f"[***] Moving {source_key} to {target_key}")
                # Copy object
                s3_client.copy_object(
                    Bucket=BUCKET,
                    Key=target_key,
                    CopySource={'Bucket': BUCKET, 'Key': source_key}
                )
                # Delete original object
                s3_client.delete_object(Bucket=BUCKET, Key=source_key)

    # CLEAN Parquet Directory
    PARQUET_PATH = parquet_key
    # Create a reusable Paginator
    paginator = s3_client.get_paginator('list_objects_v2')
    # Create a PageIterator from the Paginator
    page_iterator = paginator.paginate(Bucket=BUCKET, Prefix=PARQUET_PATH)
    # Loop through each object, looking for ones older than a given time period
    for page in page_iterator:
        if 'Contents' in page:
            for object in page['Contents']:
                if object['LastModified'] < dt.now().astimezone() - timedelta(days=3):  # <-- Change time period here
                    source_key = object['Key']
                    if not source_key.lower().endswith('.parquet'):
                        continue
                    s3_client.delete_object(Bucket=BUCKET, Key=source_key)
