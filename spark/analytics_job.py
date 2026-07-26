from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# -------------------------------
# Create Spark Session
# -------------------------------
spark = SparkSession.builder \
    .appName("Food Delivery Analytics") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# -------------------------------
# Read Data Lake (Parquet)
# -------------------------------
orders_df = spark.read.parquet(
    "/app/data/processed/data_lake/orders"
)

# -------------------------------
# Basic Cleaning
# -------------------------------
orders_df = orders_df.dropDuplicates(["order_id"])

orders_df = orders_df.filter(
    col("order_value").isNotNull()
)

# -------------------------------
# Revenue by Restaurant
# -------------------------------
restaurant_revenue = (
    orders_df
    .groupBy("restaurant_id", "name")
    .agg(
        sum("order_value").alias("total_revenue"),
        count("order_id").alias("total_orders"),
        avg("delivery_time").alias("avg_delivery_time")
    )
)

# -------------------------------
# Revenue by City
# -------------------------------
city_revenue = (
    orders_df
    .groupBy("city")
    .agg(
        sum("order_value").alias("total_revenue"),
        count("order_id").alias("total_orders")
    )
)

# -------------------------------
# Order Status Analysis
# -------------------------------
status_analysis = (
    orders_df
    .groupBy("status")
    .agg(
        count("*").alias("total_orders")
    )
)

# -------------------------------
# Delivery Performance
# -------------------------------
delivery_metrics = (
    orders_df
    .agg(
        avg("delivery_time").alias("avg_delivery_time"),
        min("delivery_time").alias("fastest_delivery"),
        max("delivery_time").alias("slowest_delivery")
    )
)

# -------------------------------
# Orders by Day
# -------------------------------
daily_orders = (
    orders_df
    .withColumn("order_date", to_date("timestamp"))
    .groupBy("order_date")
    .agg(
        count("*").alias("orders"),
        sum("order_value").alias("daily_revenue")
    )
)

# -------------------------------
# PostgreSQL Connection
# -------------------------------
jdbc_url = "jdbc:postgresql://host.docker.internal:5432/food_delivery"

connection_properties = {
    "user": "postgres",
    "password": "YOUR_PASSWORD",
    "driver": "org.postgresql.Driver"
}

# -------------------------------
# Write Tables
# -------------------------------

restaurant_revenue.write \
    .jdbc(
        url=jdbc_url,
        table="restaurant_revenue",
        mode="overwrite",
        properties=connection_properties
    )

city_revenue.write \
    .jdbc(
        url=jdbc_url,
        table="city_revenue",
        mode="overwrite",
        properties=connection_properties
    )

status_analysis.write \
    .jdbc(
        url=jdbc_url,
        table="status_analysis",
        mode="overwrite",
        properties=connection_properties
    )

delivery_metrics.write \
    .jdbc(
        url=jdbc_url,
        table="delivery_metrics",
        mode="overwrite",
        properties=connection_properties
    )

daily_orders.write \
    .jdbc(
        url=jdbc_url,
        table="daily_orders",
        mode="overwrite",
        properties=connection_properties
    )

print("Analytics successfully written to PostgreSQL.")

spark.stop()