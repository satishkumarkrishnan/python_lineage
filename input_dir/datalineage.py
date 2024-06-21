import io
import json
import pandas as pd
import pyspark
import boto3
from pyspark import conf
from awsglue.context import GlueContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
<<<<<<< HEAD:main.py
import boto3

#from boto3_fixtures.contrib import boto3
from urllib3 import packages
=======
from pyspark import SparkContext
>>>>>>> dd35190f88798b27eb544a59d16bd609bfa5f0c7:input_dir/datalineage.py

sc =SparkContext.getOrCreate()
sc.setLogLevel("DEBUG")
 
spark = (SparkSession.builder.master('local').appName('Python Spark SQL basic example')         
         .config('spark.some.config.option', 'some-value')
         .config('spark.openlineage.transport.type', 'http')
         .config('spark.extraListeners', 'io.openlineage.spark.agent.OpenLineageSparkListener')
         .config('spark.openlineage.transport.type', 'http')
         .config('spark.openlineage.transport.url', 'http://localhost:80')
         .config('spark.openlineage.namespace', 'spark_namespace')
         .config('spark.openlineage.parentJobNamespace', 'airflow_namespace')
         .config('spark.openlineage.parentJobName', 'airflow_dag.airflow_task')
         .config('spark.openlineage.parentRunId', 'xxxx-xxxx-xxxx-xxxx')
         .getOrCreate())
 
         
# Your Spark job code
<<<<<<< HEAD:main.py
input_path = "C:\\spark-3.4.3-bin-hadoop3\\test.csv"
output_path = "C:\\spark-3.4.3-bin-hadoop3\\output.csv"
df = spark.read.csv(input_path, header=True)
third_column = df.columns[2]
age = 40

filtered_df = df.filter(df["age"] >= 40)
filtered_df.show()

filtered_df.write.csv("C:\\spark-3.4.3-bin-hadoop3\\filtered_data.csv", header=True)
=======
input_path = "s3://ddsl-rawdata-bucket/test.csv"
output_path = "s3://ddsl-extension-bucket/output.csv"
df = spark.read.csv(input_path, header=True)
first_column = df.columns[0]
number = 200
df_transformed = df.filter(col(first_column) >= number)
df_transformed.write.mode('overwrite').csv(output_path, header=True)
df.show()
df.write.csv("s3://ddsl-extension-bucket/data_lineage.csv")
>>>>>>> dd35190f88798b27eb544a59d16bd609bfa5f0c7:input_dir/datalineage.py
lineage_data = {
    "job_name": "YourSparkJob",
    "inputs": [input_path],
    "outputs": [output_path],
}
lineage_json = json.dumps(lineage_data)
<<<<<<< HEAD:main.py
# Initialize Glue client
glue = boto3.client('glue')

# Example S3 location to store lineage information
s3_bucket = 's3://ddsl-extension-bucket/'
s3_key = 'lineage.json'

# Upload lineage JSON to S3
#glue.put_data_catalog_lineage_settings(CatalogId='your-catalog-id', LineageSettings={"LineageData": lineage_json})
=======

# Example S3 location to store lineage information
s3_bucket = 's3://ddsl-extension-bucket'
s3_key = 'lineage.json'

# Upload lineage JSON to S3
df.write.format('json').save('s3://ddsl-extension-bucket/lineage.json')
>>>>>>> dd35190f88798b27eb544a59d16bd609bfa5f0c7:input_dir/datalineage.py
spark.stop()