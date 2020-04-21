# Unit Challenge

Challenge for OutSystems DevOps Experts.

## Solution Outline

This is a description of the main steps taken to solve the challenge.


#### AWS

1. Created an S3 bucket (`iislogs-upload)` to upload the IIS log files to.

2. Created a Lambda function (`iislogs-importer`) triggered by "All object create events" in the S3 bucket.
<br/>Used the provided Python code with some minor changes.
<br/>Gave it 128 MB memory and a 30 sec timeout.
<br/>Source code is available [here](aws/iislogs-lambda.py).

3. Created a CloudWatch log group (`/aws/lambda/iislogs-importer`) for the Lambda function to write into.

4. Created a Role (`iislogs-role`) to grant the Lambda function access to the S3 bucket and CloudWatch Logs.
<br/>The role actually uses a policy for that (`iislogs-policy`), which restricts the access to the aforementioned S3 bucket and CloudWatch log group.

5. Created a CloudFormation template to automate the creation (and deletion) of all of the above.
<br/>Source code is available [here](aws/iislogs-cloudformation-template.yml).

#### Functionbeat

1. Configured Functionbeat to:
  * Use the index lifecycle management (ILM) feature in Elasticsearch
  * Not touch the index template
  * Use an ingest pipeline in Elasticsearch
<br/>Full configuration file is available [here](functionbeat/functionbeat.yml).

#### Elastic Cloud

1. Created a template for all `iislogs*` indexes in Elasticsearch.
<br/>Source code is available [here](elasticsearch/iislogs-template.json).

2. Created an ingest pipeline to set the IIS date and time (present in the log file that is uploaded) as the `@timestamp` field for the Elasticsearch documents.
<br/>Source code is available [here](elasticsearch/iislogs-ingest-pipeline.json).

3. Created the `iislogs*` index pattern in Kibana and a dashboard that puts the 2 requested visualisations together.
<br/>Created user `dashboard_user` to access Kibana and see this dashboard. Password provided via a separate channel.

> To view data in the Kibana dashboard, make sure to set the time range to `Jul 20, 2019 @ 00:00:00.000 → Jul 20, 2019 @ 23:30:00.00`, as this is the time range for the data in the example log file that was made available [here](https://drive.google.com/file/d/1IM35NB2saAtv4ZcOXhNj9iE0yYO9o4am/view?usp=sharing).

## Room for Improvements

For a better production grade solution, some improvements can be made.

1. Take the code of the Labmbda function out of the CloudFormation template file.
<br/>The Labmbda function code was copied and pasted as inline in the CloudFormation template file.
