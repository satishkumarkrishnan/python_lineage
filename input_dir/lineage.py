from pyspark.sql import SparkSession
from pyspark import conf
from awsglue.context import GlueContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark import SparkContext
import json
import boto3

sc =SparkContext.getOrCreate()
sc.setLogLevel("DEBUG")

spark = SparkSession.builder \
    .appName("OpenLineageExample") \
    .config("spark.jars.packages", "io.openlineage:openlineage-spark_2.12-1.13.1") \
    .config("spark.extraListeners", "io.openlineage.spark.agent.OpenLineageSparkListener") \
    .config('spark.openlineage.transport.type', 'http') \
    .config('spark.openlineage.transport.url', 'http://ddsl-alb-543221022.ap-northeast-1.elb.amazonaws.com:8080') \
    .config('spark.openlineage.transport.endpoint', '/api/v1/lineage') \
    .config('spark.openlineage.namespace', 'spark_integration') \
    .getOrCreate()   

# Your Spark job code
input_path = "s3://ddsl-rawdata-bucket/test.csv"
output_path = "s3://ddsl-extension-bucket/dlineage"

# Read CSV file
df = spark.read.csv(input_path, header=True)

# Filter DataFrame based on the third column's values being greater than or equal to 40
third_column = df.columns[2]
df_transformed = df.filter(df[third_column] >= 40)

# Write transformed DataFrame to a new CSV file
df_transformed.write.csv(output_path, mode="overwrite", header=True)

# Show original and filtered DataFrames
df.show()
filtered_df = df.filter(df[third_column] >= 40)
filtered_df.show()

# Collect detailed schema information for lineage
schema_fields = [{"name": field.name, "type": str(field.dataType)} for field in df.schema.fields]

lineage_df = {
    "job_name": "YourSparkJob",
    "inputs": [{
        "namespace": "file",
        "name": input_path,
        "facets": {
            "dataSource": {
                "_producer": "https://github.com/OpenLineage/OpenLineage/tree/1.13.1/integration/spark",
                "_schemaURL": "https://openlineage.io/spec/facets/1-0-1/DatasourceDatasetFacet.json#/$defs/DatasourceDatasetFacet",
                "name": "file",
                "uri": input_path
            },
            "schema": {
                "_producer": "https://github.com/OpenLineage/OpenLineage/tree/1.13.1/integration/spark",
                "_schemaURL": "https://openlineage.io/spec/facets/1-1-1/SchemaDatasetFacet.json#/$defs/SchemaDatasetFacet",
                "fields": schema_fields
            }
        },
        "inputFacets": {}
    }],
    "outputs": [{
        "namespace": "file",
        "name": output_path,
        "facets": {
            "dataSource": {
                "_producer": "https://github.com/OpenLineage/OpenLineage/tree/1.13.1/integration/spark",
                "_schemaURL": "https://openlineage.io/spec/facets/1-0-1/DatasourceDatasetFacet.json#/$defs/DatasourceDatasetFacet",
                "name": "file",
                "uri": output_path
            },
            "schema": {
                "_producer": "https://github.com/OpenLineage/OpenLineage/tree/1.13.1/integration/spark",
                "_schemaURL": "https://openlineage.io/spec/facets/1-1-1/SchemaDatasetFacet.json#/$defs/SchemaDatasetFacet",
                "fields": schema_fields
            }
        },
        "outputFacets": {}
    }]
}

# Convert dictionary to JSON string
lineage_json = json.dumps(lineage_df, indent=4)

# Optional: Upload lineage JSON to S3 (commented out)
# Initialize Glue client
s3 = boto3.client('s3')

# Example S3 location to store lineage information
s3_bucket = 'ddsl-extension-bucket'
s3.put_object( Bucket=s3_bucket, Key='lineage.json', Body=lineage_json.encode('utf-8'))

# Stop Spark session
spark.stop()