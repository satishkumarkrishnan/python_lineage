import io
import json
import pandas as pd
import pyspark
import boto3
from pyspark import conf
from awsglue.context import GlueContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark import SparkContext

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
input_path = "s3://ddsl-rawdata-bucket/test.csv"
output_path = "s3://ddsl-extension-bucket/output.csv"
df = spark.read.csv(input_path, header=True)
first_column = df.columns[0]
number = 200
df_transformed = df.filter(col(first_column) >= number)
df_transformed.write.mode('overwrite').csv(output_path, header=True)
df.show()
df.write.csv("s3://ddsl-extension-bucket/data_lineage.csv")
lineage_data = {
    "job_name": "YourSparkJob",
    "inputs": [input_path],
    "outputs": [output_path],
}
lineage_json = json.dumps(lineage_data)

# Example S3 location to store lineage information
s3_bucket = 's3://ddsl-extension-bucket'
s3_key = 'lineage.json'

# Upload lineage JSON to S3
df.write.format('json').save('s3://ddsl-extension-bucket/lineage.json')
spark.stop()