## Simple Feedback Form - HTML, Lambda, API gateway & cloud Elastic APM

This is a simple feedback form using HTML & CSS 
1. HTML will send a POST request to API Gateway. The form content are sent through query string in the URL. Initially required query string parameter are validated using API gateway service
2. Lambda will furthur collect the information from events and send to RDS (storage) and SES service (email form details)
3. Cloud Elastic APM is added for stack tracing (This includes only APM and RUM funcationality in elastic observability. Refer Other elatic product to collect logs, audit, securty, host metric etc)

## Elastic APM: 
Below snippet is used to send apm data to cloud elastic. modify the connection details.
service name is required and it is used to track apm data in kibana 
get secret token from ES for authentication
Elastic APM will record the transaction from the start of lambda_handler till end which involves transaction processing time, error, stack trace etc

client = Client(
    {
        'SERVER_URL': 'https://xxxxxxxxxxxxxxxxxxxxxxx.apm.us-east-1.aws.cloud.es.io:443',
        'SERVICE_NAME': 'DemoFlask2',
        'ENVIRONMENT': 'dev',
        'SECRET_TOKEN': ''
    }
)

## Elastic RUM
This is used to get front end website performance like page load time, dom processing etc
<script>
  elasticApm.init({
    serviceName: 'feedback-rum',
    serverUrl: 'https://xxxxxxxxxxxxxxxxxxxxxxxxxxx.apm.us-east-1.aws.cloud.es.io:443',
  })
</script>
replace the serverurl with elastic cloud url and servicename to your wish

client.begin_transaction('request')
def lambda_handler(event, context):
    ............
client.end_transaction('feedback-transaction', 'success')

## HTML: 
In index.html change the URL of api gateway in form actions 
<div class="enquiry_form">
  <form action="https://xxxxxxxxxxxxxxxxxxxxxx-api-endpoint.com">

## schemas.js 
This is a schema to validate the parameters 
refer below link for more info on this package 
https://json-schema.org/understanding-json-schema/
https://json-schema.org/learn/getting-started-step-by-step.html#data
https://awslabs.github.io/aws-lambda-powertools-python/latest/utilities/validation/

## test.py
contains test json to validate the program funtionality before deploying to cloud 
change the data according to your needs 
remove # from #print(lambda_handler(event,context)) in app.py to run the python locally - step not required to run in aws lambda

## app.py
This is the lambda function using python to get query paramters, validate and send to rds and ses service for notification and storage of info
rds_host  = "rds-instance-endpoint"
name = "db_username"
password = "db_password"
db_name = "db_name"
recepient_email = "test@gmail.com"
sender_email = "test@gmail.com"

modify the above variables to authenticate RDS and verify the ses sender email once to make ses service active
refer secrets manager service (cost involed for storing per secret) to store cred in the SM and access in this python lambda using boto library  

# To deploy this lambda function in AWS
1. install the requirement in local folder - pip install -r requirements.txt -t ./package
2. move app.py schemas.py to ./package folder
3. cd into ./pakcage folder
4. make a zip of the content in the folder and upload it to lambda
5. change api gateway endpoint & apm elastic endpoints in html and deploy site in either s3/ec2/docker what ever works for you 

## terraform - WIP
terraform file will provision resources like aws pipeline, s3 for storing artifacts, api-gateway, RDS, SES and lambda