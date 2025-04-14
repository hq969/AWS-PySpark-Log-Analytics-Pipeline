from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StringType, TimestampType

# 1. Start Spark Session
spark = SparkSession.builder \
    .appName("KinesisLogAnalytics") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# 2. Define Log Schema
log_schema = StructType() \
    .add("timestamp", TimestampType()) \
    .add("ip", StringType()) \
    .add("method", StringType()) \
    .add("endpoint", StringType()) \
    .add("status", StringType())

# 3. Read from Kinesis Stream
kinesis_stream = spark.readStream \
    .format("kinesis") \
    .option("streamName", "your-kinesis-stream-name") \
    .option("region", "us-east-1") \
    .option("initialPosition", "LATEST") \
    .load()

# 4. Parse JSON logs
json_logs = kinesis_stream.selectExpr("CAST(data AS STRING) as json_string") \
    .select(from_json(col("json_string"), log_schema).alias("log")) \
    .select("log.*")

# 5. Perform aggregations
log_summary = json_logs \
    .withWatermark("timestamp", "1 minute") \
    .groupBy(
        window(col("timestamp"), "1 minute"),
        col("status")
    ).count()

# 6. Write output to S3
query = log_summary.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("checkpointLocation", "s3://your-bucket/checkpoints/") \
    .option("path", "s3://your-bucket/processed-logs/") \
    .trigger(processingTime="60 seconds") \
    .start()

query.awaitTermination()
