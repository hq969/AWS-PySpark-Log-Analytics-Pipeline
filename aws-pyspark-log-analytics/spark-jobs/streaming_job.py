from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StringType, TimestampType
import json

# === Load Config ===
with open("config/spark_config.json") as config_file:
    config = json.load(config_file)

APP_NAME = config["app_name"]
REGION = config["region"]
STREAM_NAME = config["stream_name"]
CHECKPOINT_PATH = config["checkpoint_path"]
OUTPUT_PATH = config["output_path"]

# === Create SparkSession ===
spark = SparkSession.builder \
    .appName(APP_NAME) \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# === Define Schema ===
log_schema = StructType() \
    .add("timestamp", TimestampType()) \
    .add("ip", StringType()) \
    .add("method", StringType()) \
    .add("endpoint", StringType()) \
    .add("status", StringType())

# === Read from Kinesis Stream ===
kinesis_df = spark.readStream \
    .format("kinesis") \
    .option("streamName", STREAM_NAME) \
    .option("region", REGION) \
    .option("initialPosition", "LATEST") \
    .load()

# === Parse and Structure Log Data ===
parsed_df = kinesis_df.selectExpr("CAST(data AS STRING) as json_data") \
    .select(from_json(col("json_data"), log_schema).alias("log")) \
    .select("log.*")

# === Aggregation: Count per status code every minute ===
aggregated_df = parsed_df \
    .withWatermark("timestamp", "1 minute") \
    .groupBy(
        window(col("timestamp"), "1 minute"),
        col("status")
    ).count()

# === Write to S3 in Parquet Format ===
query = aggregated_df.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("checkpointLocation", CHECKPOINT_PATH) \
    .option("path", OUTPUT_PATH) \
    .trigger(processingTime="60 seconds") \
    .start()

query.awaitTermination()
