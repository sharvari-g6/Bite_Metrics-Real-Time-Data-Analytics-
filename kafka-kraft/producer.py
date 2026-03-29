import json
import time
import random
import pandas as pd
from kafka import KafkaProducer
from datetime import datetime

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Load cleaned dataset
orders_df = pd.read_csv("C:/DE project/data/processed/orders_cleaned.csv")

# Load restaurants dataset (IMPORTANT for join)
restaurants_df = pd.read_csv("C:/DE project/data/processed/restaurants_cleaned.csv")

# Get valid restaurant IDs
restaurant_ids = restaurants_df["restaurant_id"].unique()

print("🚀 Streaming started...")

while True:
    # Pick random order
    row = orders_df.sample(1).iloc[0]

    # Ensure valid restaurant_id
    restaurant_id = random.choice(restaurant_ids)

    message = {
        "order_id": str(row["order_id"]),
        "order_value": float(row["order_value"]),
        "status": str(row["status"]),
        "delivery_time": float(row["delivery_time"]),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "restaurant_id": str(restaurant_id)  # IMPORTANT FIX
    }

    producer.send("food_orders", value=message)
    print("Sent:", message)

    time.sleep(2)  # simulate real-time delay