import pandas as pd
import random
from datetime import datetime, timedelta

# Load restaurant data
restaurants_df = pd.read_csv("data/processed/restaurants_cleaned.csv")

# Get valid restaurant IDs
restaurant_ids = restaurants_df["restaurant_id"].values

orders = []

# Generate 1000 historical orders
for i in range(1000):
    order = {
        "order_id": f"O{i+1}",
        "order_value": random.randint(100, 500),
        "status": random.choice(["delivered", "cancelled"]),
        "delivery_time": random.randint(20, 60),
        "timestamp": (
            datetime.now() - timedelta(days=random.randint(1, 30))
        ).strftime("%Y-%m-%d %H:%M:%S"),
        "restaurant_id": random.choice(restaurant_ids)
    }
    orders.append(order)

# Convert to DataFrame
orders_df = pd.DataFrame(orders)

# Save CSV
orders_df.to_csv("data/processed/orders_cleaned.csv", index=False)

print("✅ Historical orders dataset created!")