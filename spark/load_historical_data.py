from pyspark.sql import SparkSession

# Create Spark Session
spark = SparkSession.builder \
    .appName("Load Historical Orders") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# -------------------------------
# STEP 1: Load Historical Orders CSV
# -------------------------------
orders_df = spark.read.csv(
    "/app/data/processed/orders_cleaned.csv",
    header=True,
    inferSchema=True
)

# -------------------------------
# STEP 2: Load Restaurants Data
# -------------------------------
restaurants_df = spark.read.csv(
    "/app/data/processed/restaurants_cleaned.csv",
    header=True,
    inferSchema=True
)

# -------------------------------
# STEP 3: Join Data
# -------------------------------
joined_df = orders_df.join(
    restaurants_df,
    on="restaurant_id",
    how="left"
)

# -------------------------------
# STEP 4: Write to Data Lake
# -------------------------------
joined_df.write \
    .format("parquet") \
    .mode("append") \
    .save("/app/data/processed/data_lake/orders")

print("✅ Historical data loaded successfully into Data Lake!")

spark.stop()