import os
import sys
import json
import logging


root = logging.getLogger()

if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)

stream_handler = logging.StreamHandler(sys.stdout)

log_args = {
    "level": logging.INFO,
    "format": "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    "datefmt": '%d-%b-%y %H:%M' ,
    "handlers": [stream_handler]
}

logging.basicConfig(**log_args)

from lib_kms import *

file_name = os.path.splitext(os.path.basename(__file__))[0]

def lambda_handler(event, context):
    
    logger = logging.getLogger(f"{file_name}.__main__")
    
    desc_kms = 'poc-kms-encrypt-decrypt'
    
    filename = 's3://dvtps3-sftp-incoming/testData.csv'
    
    KeyId, KeyArn = retrieve_cmk(desc_kms)
    
    logger.info(f'[*] Retrieve Customer Master Key (CMK) = KeyId {KeyId}, KeyArn {KeyArn}')
    
    if not KeyId and not KeyArn:
        logger.info('[+] Creating new master key')
        KeyId, KeyArn = create_cmk(desc_kms)
        logger.info(f'[*] Create Master Key = KeyId {KeyId}, KeyArn {KeyArn}')
    
    if not KeyId and not KeyArn:
        logger.error('[-] Customer Master Key (CMK) cannot be none')
        raise 
    
    EncryptedDataKey, PlaintextDataKey = create_data_key(cmk_id = KeyId, key_spec='AES_256')
    logger.info(f'[*] Create Data Key = EncryptedDataKey {EncryptedDataKey}, PlaintextDataKey {PlaintextDataKey}')

    if encrypt_file(filename, cmk_id = KeyId):
        logger.info('[+] file encrypted')
    else:
        logger.error('[-] file  is not encrypted')
        raise
    
    if decrypt_file(filename ):
        logger.info('[+] file decrypted')
    else:
        logger.error('[-] file  is not decrypted')
        raise
        
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Demo Success !')
    }
