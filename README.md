# Real-time Analytics: Designing a Streaming Data Ingestion Platform Natively on AWS


In this project, I utilized an AWS-based pipeline involving AWS Kinesis, Glue, and Athena to perform real-time analytics of mobile coverage using PySpark. The following is the AWS architecture for this project:

![AWS Architecture](/images/unknown.png)

The system will stream logs from Amazon Kinesis, process them using AWS Glue with PySpark, and perform data aggregation for advanced analytics.

## Initial Setup

In the initial phase, we set up two S3 buckets: one for storing the input dataset and another for storing the output of the Spark streaming job on AWS Glue.

![S3 Buckets](/images/s3.png)

Next, we set up the Kinesis Data Stream.

![Kinesis Data Stream](/images/kinesis-data-viewer.png)

We had to ensure that we created IAM roles for Lambda and Glue to allow these services to access the S3 bucket, Kinesis, Lambda, and Glue.

## Lambda Function

We created a Lambda function to process CSV files uploaded to the S3 bucket and send the data to the Kinesis stream.

![Lambda Function](/images/lambda.png)

We added a trigger to the Lambda function that will call the Lambda when a CSV file is uploaded to the S3 bucket.

## AWS Glue ETL Job

We created an ETL job on Glue and added the PySpark streaming code to AWS Glue.

![Glue ETL Job](/images/glue-etl-job.png)


Pyspark streaming code sets up a robust streaming data analysis pipeline that continuously processes incoming data from a Kinesis stream, performs aggregations, and writes the results to S3.

When a CSV file is uploaded to the S3 bucket, it streams it to Kinesis, processes it on Glue, and uploads the output to S3. Below, you can see the CloudWatch logs when the CSV was uploaded.

![CloudWatch Logs](/images/lambda-cloudwatch.png)

The file created after the ETL job is completed:

![Output File](/images/after_etl.png)

## Data Analysis with Athena

For data analysis, I utilized AWS Glue crawlers and then used Athena to execute SQL queries on the data tables generated by Glue crawlers.

![Athena Query](/images/athena.png)

By utilizing this AWS-based pipeline, I was able to analyze the data and get valuable insights from it.