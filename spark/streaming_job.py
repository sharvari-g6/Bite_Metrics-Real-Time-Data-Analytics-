from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Create Spark Session
spark = SparkSession.builder \
    .appName("Food Delivery Streaming") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# -------------------------------
# STEP 1: Load Kafka Stream
# -------------------------------
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "host.docker.internal:9092") \
    .option("subscribe", "food_orders") \
    .option("startingOffsets", "latest") \
    .load()

kafka_df = kafka_df.selectExpr("CAST(value AS STRING)")

# -------------------------------
# STEP 2: Define Schema
# -------------------------------
schema = StructType([
    StructField("order_id", StringType()),
    StructField("order_value", FloatType()),
    StructField("status", StringType()),
    StructField("delivery_time", FloatType()),
    StructField("timestamp", StringType()),
    StructField("restaurant_id", StringType())
])

# -------------------------------
# STEP 3: Parse JSON
# -------------------------------
orders_df = kafka_df \
    .withColumn("data", from_json(col("value"), schema)) \
    .select("data.*")

orders_df = orders_df.withColumn(
    "timestamp",
    to_timestamp("timestamp")
)

# -------------------------------
# STEP 4: Load Static Data
# -------------------------------
restaurants_df = spark.read.csv(
    "/app/data/processed/restaurants_cleaned.csv",
    header=True,
    inferSchema=True
)

# -------------------------------
# STEP 5: Join
# -------------------------------
joined_df = orders_df.join(
    restaurants_df,
    on="restaurant_id",
    how="left"
)

# -------------------------------
# STEP 6: Write to Data Lake
# -------------------------------
query = joined_df.writeStream \
    .format("parquet") \
    .option("path", "/app/data/processed/data_lake/orders") \
    .option("checkpointLocation", "/app/data/checkpoints/parquet_orders") \
    .outputMode("append") \
    .start()

# -------------------------------
# STEP 7: Keep Running
# -------------------------------
query.awaitTermination()