

I have an AWS Lambda that is triggered through API Gateway set up with the following code:

import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('sns')

    response = client.publish(
        TargetArn='arn:aws:sns:us-east-1:264604750251:Billing_SubscriptionMessage_1',
        Message=json.dumps({'default': json.dumps(event['body'])}),
        MessageStructure='json'
    )
   
    return response
