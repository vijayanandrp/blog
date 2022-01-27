url - https://medium.com/taptuit/add-notifications-to-your-aws-ci-cd-pipeline-251bba894360


```yaml
  TeamsURL:
    Description: "Incoming Microsoft Teams Webhook URL"
    Type: String
    Default: "Your-Microsoft-Teams-Incoming-Webhook-URL"
 
  CodePipelineName:
    Description: "Codepipeline Name"
    Type: String
    Default: "Your-Codepipeline-Name" 
```

``` yaml
NotificationLambdaFunction:
  Type: 'AWS::Lambda::Function'
  Properties:
    Handler: index.index_handler
    Code:
      ZipFile: |
        import urllib3
        import json
        import os
        http = urllib3.PoolManager()
        def index_handler(event, context):
            url = os.environ['TEAMS_URL']
            event_message = event['Records'][0]['Sns']['Message']
            message_dict  = json.loads(event_message)
            pipeline_name = message_dict["detail"]["pipeline"]
            pipeline_status = message_dict["detail"]["state"]
            print(pipeline_name)

            msg = {
                "text": f"Pipeline: {pipeline_name} has: {pipeline_status}"
            }

            encoded_msg = json.dumps(msg).encode('utf-8')
            resp = http.request('POST',url, body=encoded_msg)
            print({
                "message": pipeline_name,
                "status_code": resp.status,
              "response": resp.data
            })
    MemorySize: 128
    Environment:
      Variables:
        TEAMS_URL: !Ref TeamsURL
    Runtime: 'python3.7'
    Timeout: 30
    Role: !GetAtt NotificationLambdaFunctioneRole.Arn

NotificationLambdaFunctioneRole:
  Type: 'AWS::IAM::Role'
  Properties:
    AssumeRolePolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Effect: Allow
          Principal:
            Service: 'lambda.amazonaws.com'
          Action: 'sts:AssumeRole'
    Policies:
      - PolicyName: 'customresource'
        PolicyDocument:
          Statement:
            - Effect: Allow
              Action:
                - 'sns:*'
              Resource: '*'
            - Effect: Allow
              Action:
                - 'logs:CreateLogGroup'
                - 'logs:CreateLogStream'
                - 'logs:PutLogEvents'
              Resource: '*'
           
EventRule:
  DependsOn: NotificationLambdaFunction
  Type: AWS::Events::Rule
  Properties:
    Description: "EventRule"
    EventPattern:
      source:
        - "aws.codepipeline"
      detail-type:
        - "CodePipeline Pipeline Execution State Change"
      detail:
        state:
          - "FAILED"
        pipeline:
          - !Ref CodePipelineName
      resources:
        - !Sub 'arn:aws:codepipeline:${AWS::Region}:${AWS::AccountId}:${CodePipelineName}'
    State: "ENABLED"
    Targets:
      -
        Arn:
          Ref: "SNSTopic"
        Id: "NotificationTeams"

PermissionLambda:
  DependsOn: NotificationLambdaFunction
  Type: AWS::Lambda::Permission
  Properties:
    FunctionName:
      Ref: "NotificationLambdaFunction"
    Action: "lambda:InvokeFunction"
    Principal: "sns.amazonaws.com"
    SourceArn: !Ref SNSTopic

SNSTopic:
  DependsOn: NotificationLambdaFunction
  Type: AWS::SNS::Topic
  Properties:
    DisplayName: String
    Subscription:
      - Protocol: lambda
        Endpoint: !GetAtt NotificationLambdaFunction.Arn

SnsTopicPolicy:
  Type: AWS::SNS::TopicPolicy
  DependsOn: SNSTopic
  Properties:
    PolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Sid: SnsTopicPolicy
          Effect: Allow
          Principal:
            AWS: "*"
          Action:
            - "SNS:GetTopicAttributes"
            - "SNS:SetTopicAttributes"
            - "SNS:AddPermission"
            - "SNS:RemovePermission"
            - "SNS:DeleteTopic"
            - "SNS:Subscribe"
            - "SNS:ListSubscriptionsByTopic"
            - "SNS:Publish"
            - "SNS:Receive"
          Resource:
            Ref: SNSTopic
        - Sid: SnsTopicPolicyEvent
          Effect: Allow
          Principal:
            Service: "events.amazonaws.com"
          Action:
            - "SNS:Publish"
          Resource:
            Ref: SNSTopic
    Topics:
      - Ref: SNSTopic
```

```python
import urllib3
import json
import os
import boto3

http = urllib3.PoolManager()


def index_handler(event, context):
    url = os.environ['TEAMS_URL']
    event_message = event['Records'][0]['Sns']['Message']
    message_dict = json.loads(event_message)
    pipeline_name = message_dict["detail"]["pipeline"]
    pipeline_status = message_dict["detail"]["state"]
    execution_id = message_dict["detail"]["execution-id"]
    text = f"Code Pipeline: {pipeline_name} with execution-id {execution_id} has: {pipeline_status}."
    title = "[Red Alert] - Code Deployment Failed"

    msg = {
        "@context": "https://schema.org/extensions",
        "@type": "MessageCard",
        "themeColor": "d63333",
        "text": text,
        "title": title,
        "sections": [{
            "facts": [{
                "name": "Pipeline",
                "value": f"{pipeline_name}"
            }, {
                "name": "Execution Id",
                "value": f"{execution_id}"
            }, {
                "name": "Status",
                "value": f"{pipeline_status}"
            }],
            "markdown": True
        }]
    }

    encoded_msg = json.dumps(msg).encode('utf-8')
    resp = http.request('POST', url, body=encoded_msg)
    print({
        "message": pipeline_name,
        "status_code": resp.status,
        "response": resp.data
    })

    message = {
        "mailContentType": "text",
        "mailBody": text,
        "mailSubject": title,
        "toAddresses": os.environ["EMAIL_LIST"]
    }

    boto3.client("sns").publish(
        TargetArn=os.environ["SNS_TOPIC"],
        Message=json.dumps(message),
    )

```
