import json
import schemas
from aws_lambda_powertools.utilities.validation import validate
from aws_lambda_powertools.utilities.validation.exceptions import SchemaValidationError
from elasticapm import Client
import sys
import logging
import rds_config
import pymysql
import boto3
from botocore.exceptions import ClientError

rds_host  = "rds-instance-endpoint"
name = "db_username"
password = "db_password"
db_name = "db_name"
recepient_email = "test@gmail.com"
sender_email = "test@gmail.com"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = Client(
    {
        'SERVER_URL': 'https://xxxxxxxxxxxxxxxxxxxxxxxx.apm.us-east-1.aws.cloud.es.io:443',
        'SERVICE_NAME': 'feedback-form',
        'ENVIRONMENT': 'prod',
        'SECRET_TOKEN': 'xxxxxxxxxxxxxxxxxxxxxxx'
    }
)

client.begin_transaction('request')
def lambda_handler(event, context):
    try:
        validate(event=event, schema=schemas.INPUT, envelope="queryStringParameters")
    except SchemaValidationError:
        client.capture_exception()
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Bad Request"}),
        }
    except:
        client.capture_exception()
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Request failed"})
        }
    
    try:
        conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        client.capture_exception()
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Request failed"})
        }
        sys.exit()

    try:
        conn.cursor().execute(
            """insert into feedback (name, country, subject) values({0},{1},{2})"""
            .format(event["queryStringParameters"]['name'], event["queryStringParameters"]['country'], event["queryStringParameters"]['subject'])
            )
        try:
            SENDER = sender_email
            RECIPIENT = recepient_email
            AWS_REGION = "us-west-2"
            SUBJECT = "new Feedback"
            BODY_HTML = """<html><body>
            new feeback from user:\n 
            name: {0} \n
            country: {1} \n
            subject: {2}
            </body></html>"""
            .format(event["queryStringParameters"]['name'], event["queryStringParameters"]['country'], event["queryStringParameters"]['subject'])
            client = boto3.client('SENDER',region_name=AWS_REGION)
            response = client.send_email(
            Destination={'ToAddresses': [RECIPIENT]},
            Message={
                'Body': {'Html': {'Data': BODY_HTML}},
                'Subject': {'Data': SUBJECT},
            },
            Source=SENDER
            )      
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:")
            print(response['MessageId'])
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "form submitted"})
            }
    except:
        client.capture_exception()
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Request failed"})
        }

client.end_transaction('feedback-transaction', 'success')

#print(lambda_handler(event,context))
