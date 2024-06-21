import io
import json
import pandas as pd
import pyspark
from pyspark import conf
from pyspark.shell import sc
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import boto3

#from boto3_fixtures.contrib import boto3
from urllib3 import packages

jar_path = "C:\spark-3.4.3-bin-hadoop3\openlineage-spark_2.12-1.13.1.jar"
spark = SparkSession.builder.getOrCreate()
sc.setLogLevel("DEBUG")
spark = (SparkSession.builder.master('local').appName('Python Spark SQL basic example')
         .config('spark.jars', jar_path)
         .config('spark.some.config.option', 'some-value')
         .config('spark.openlineage.transport.type', 'http')
         .config('spark.extraListeners', 'io.openlineage.spark.agent.OpenLineageSparkListener')
         .config('spark.openlineage.transport.type', 'http')
         .config('spark.openlineage.transport.url', 'http://localhost:8080')
         .config('spark.openlineage.namespace', 'spark_namespace')
         .config('spark.openlineage.parentJobNamespace', 'airflow_namespace')
         .config('spark.openlineage.parentJobName', 'airflow_dag.airflow_task')
         .config('spark.openlineage.parentRunId', 'xxxx-xxxx-xxxx-xxxx')
         .getOrCreate())

# Your Spark job code
input_path = "C:\\spark-3.4.3-bin-hadoop3\\test.csv"
output_path = "C:\\spark-3.4.3-bin-hadoop3\\output.csv"
df = spark.read.csv(input_path, header=True)
third_column = df.columns[2]
age = 40

filtered_df = df.filter(df["age"] >= 40)
filtered_df.show()

filtered_df.write.csv("C:\\spark-3.4.3-bin-hadoop3\\filtered_data.csv", header=True)
lineage_data = {
    "job_name": "YourSparkJob",
    "inputs": [input_path],
    "outputs": [output_path],
}
lineage_json = json.dumps(lineage_data)
# Initialize Glue client
glue = boto3.client('glue')

# Example S3 location to store lineage information
s3_bucket = 's3://ddsl-extension-bucket/'
s3_key = 'lineage.json'

# Upload lineage JSON to S3
#glue.put_data_catalog_lineage_settings(CatalogId='your-catalog-id', LineageSettings={"LineageData": lineage_json})
spark.stop()