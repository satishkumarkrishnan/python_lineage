import io
import json
import pandas as pd
import pyspark
from pyspark import conf
from pyspark.shell import sc
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

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
#df = spark.read.csv(input_path, header=True)
df = spark.read.csv(input_path, header=True)
# df_transformed = df.withColumn("Column1[0]")
# df_transformed.write.csv(output_path, mode="overwrite", header=True)
first_column = df.columns[0]
number = 200
df_transformed = df.filter(col(first_column) >= number)
df_transformed.write.mode('overwrite').csv(output_path, header=True)
df.show()
df.write.csv("C:\\spark-3.4.3-bin-hadoop3\\data_lineage.csv")
lineage_data = {
    "job_name": "YourSparkJob",
    "inputs": [input_path],
    "outputs": [output_path],
}
lineage_json = json.dumps(lineage_data)
# Initialize Glue client
# glue = boto3.client('glue')

# Example S3 location to store lineage information
# s3_bucket = 's3://ddsl-extension-bucket/'
# s3_key = 'lineage.json'

# Upload lineage JSON to S3
# glue.put_data_catalog_lineage_settings(CatalogId='your-catalog-id', LineageSettings={"LineageData": lineage_json})
spark.stop()