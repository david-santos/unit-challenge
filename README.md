# Unit Challenge

Challenge for OutSystems DevOps Experts.

## Steps Taken

1. Created an AWS S3 bucket called `my-iislogs`.

2. Created an AWS Lambda function triggered by a S3 "All object create events".
<br/>Used the provided Python code but did some small changes.
<br/>Gave it 128 MB memory and a 30 sec timeout.
<br/>Source code is available [here](aws/lambda/lambda_function.py).

3. Created an AWS Role named `lambda-s3-cloudwatch-iislogs` to grant the Lambda function access to the S3 bucket and AWS CloudWatch Logs.
<br/>This role uses a policy that restricts the access to the `my-iislogs` S3 bucket and the `/aws/lambda/s3-to-cloudwatch` CloudWatch log group.
<br/>Source code for the policy is available [here](aws/policy/AWSLambdaS3CloudWatchLogsPolicy.json).

4. Configured Functionbeat to use the index lifecycle management (ILM) feature in Elasticsearch, not touch the index template and use an ingest pipeline.
<br/>Full configuration file is available [here](functionbeat/functionbeat.yml).

5. Created a template for all `iislogs*` indexes in Elasticsearch.
<br/>Source code is available [here](elasticsearch/iislogs-template.json).

6. Created an ingest pipeline to set the IIS date and time as the Elasticsearch document `@timestamp` field.
<br/>Source code is available [here](elasticsearch/iislogs-ingest-pipeline.json).

7. Created the `iislogs*` index pattern in Kibana and a dashboard that puts the 2 requested visualisations together.
<br/>Created user `dashboard_user` to access Kibana and see this dashboard.

> To view data in the Kibana dashboard, make sure to set the time range to `Jul 20, 2019 @ 00:00:00.000 → Jul 20, 2019 @ 23:30:00.00`.

## Room for Improvements

1. Use AWS CloudFormation to have an automatic and declarative way of setting up the S3 bucket, the role and the Labmbda function.

