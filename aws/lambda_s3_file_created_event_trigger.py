import boto3
import os
import logging

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
        log.info(f'New File - {new_file}')

        try:
            source = new_file['key'].split('/')[1]
            report = new_file['key'].split('/')[2]
            date = new_file['key'].split('/')[3].replace('date=', '')
        except Exception as error:
            log.warning(f"[-] String split error - {str(error)}")
            continue

        arguments = {
            '--SOURCE': source,
            '--REPORT': report,
            '--DATE': date,
            '--BUCKET': new_file['bucket'],
            '--KEY': new_file['key'],
            '--SIZE': new_file['size'],
        }
        log.info(f'arguments - {arguments}')

        response = glue.start_job_run(
            JobName='insights_glue',
            Arguments=arguments,
            Timeout=2660,
            NotificationProperty={})
        log.info(f"[*] response - {response}")

    log.info('=' * 30 + " Exit " + '=' * 30)
    return
