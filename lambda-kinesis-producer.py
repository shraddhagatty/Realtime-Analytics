import json
import csv
import boto3
import logging
from io import StringIO

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Specify AWS region
aws_region = "us-east-1"

def lambda_handler(event, context):
    # Initialize AWS clients with specified region
    s3_client = boto3.client('s3', region_name=aws_region)
    kinesis_client = boto3.client('kinesis', region_name=aws_region)

    # Extract bucket name and file name from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']

    logger.info(f"Received event for file: {file_name} in bucket: {bucket_name}")

    # Get the file from S3
    try:
        obj = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        file_content = obj['Body'].read().decode('utf-8')
    except Exception as e:
        logger.error(f"Error getting file {file_name} from bucket {bucket_name}: {e}")
        raise e

    # Read the file content using csv.DictReader
    csv_data = StringIO(file_content)
    csv_reader = csv.DictReader(csv_data)

    counter = 0
    batch_size = 100
    for row in csv_reader:
        try:
            response = kinesis_client.put_record(
                StreamName="mobile_coverage_logs",
                Data=json.dumps(row),
                PartitionKey=str(hash(row['hour']))
            )

            counter += 1

            # Check response status
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                logger.error('Error sending message to Kinesis:', response)

            # Log after every batch_size records
            if counter % batch_size == 0:
                logger.info(f"Processed {counter} records so far...")

        except Exception as e:
            logger.error(f"Error processing record {row}: {e}")

    logger.info(f"Finished processing. Total records sent: {counter}")
    return {
        'statusCode': 200,
        'body': json.dumps(f"Processed {counter} records from {file_name} in S3 bucket {bucket_name}.")
    }