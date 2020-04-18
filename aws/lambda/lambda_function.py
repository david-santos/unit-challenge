import logging
from urllib.parse import unquote_plus

import boto3
import botocore

logger = logging.getLogger()
logging.getLogger().setLevel(logging.INFO)

def lambda_handler(event, context) :
    """Processes S3 put events and dumps the files content to cloudwatch logs"""

    records = event.get('Records', [])
    if not records:
        logger.warning("no records found")
        return

    logger.debug(f"processing {len(records)} file(s)")
    s3 = boto3.client('s3')
    for record in records:
        _dump_file(s3, record)


def _dump_file(s3, record):
    """Dumps an s3 file to cloudwatch logs"""

    try:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])

        logger.debug(f"handling file {key}")
        s3_object = s3.get_object(Bucket=bucket, Key=key)

        # using iter_lines allow to stream large files in s3
        # https://kokes.github.io/blog/2018/07/26/s3-objects-streaming-python.html
        iter_lines = s3_object['Body'].iter_lines()
        for line in iter_lines:
            _dump_line(line)

        s3.delete_object(Bucket=bucket, Key=key)
        logger.debug(f"file {key} deleted")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            logger.error(f"file not found: {key}")
        else:
            raise # something else has gone wrong


def _dump_line(line):
    """Dumps a single line to cloudwatch logs"""

    logger.info(line.decode("utf-8"))
