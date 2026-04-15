# Bite Metrics – Real-Time Food Delivery Analytics Pipeline

## Overview

**Bite Metrics** is an end-to-end **real-time data engineering and analytics pipeline** built using modern big data tools. The project simulates a food delivery platform (like Zomato/Swiggy) and processes both **historical and real-time data** to generate actionable insights.

This project demonstrates concepts from:

* Data Engineering
* Streaming Systems
* Big Data Processing
* Data Warehousing
* Business Intelligence

---

## Objectives

* Transform raw dataset into structured analytical data
* Simulate real-time food order streaming
* Build a scalable streaming pipeline using Kafka
* Process data using PySpark (batch + streaming)
* Store processed data in a Data Lake and PostgreSQL
* Visualize insights using Power BI

---

## Architecture

```
Zomato Dataset
      ↓
Data Cleaning (EDA)
      ↓
restaurants_cleaned.csv  (Dimension Table)
      ↓
Synthetic Data Generation
      ↓
orders_cleaned.csv (Historical Fact Table)
      ↓
Kafka Producer → Kafka Topic (food_orders)
      ↓
PySpark Structured Streaming
      ↓
Join with restaurants_cleaned
      ↓
Processed Data
   ↙           ↘
Parquet       PostgreSQL
(Data Lake)   (BI Layer)
      ↓
   Power BI Dashboard
```

---

## Tech Stack

* **Python** – Data generation & preprocessing
* **Apache Kafka (Docker)** – Real-time streaming
* **PySpark (Docker)** – Stream & batch processing
* **PostgreSQL** – Data storage for analytics
* **Power BI** – Visualization
* **Docker** – Containerization

---

## Data Pipeline Details

### 1️⃣ Data Cleaning (Static Dataset)

* Source: Zomato dataset
* Performed:

  * Missing value handling
  * Data normalization
  * Column standardization

Output:

```
data/processed/restaurants_cleaned.csv
```

Acts as **Dimension Table**

---

### 2️⃣ Historical Data Generation

Since order-level data was unavailable, synthetic data was created:

* Randomized:

  * Order value
  * Delivery time
  * Status (delivered/cancelled)
  * Timestamp (last 30 days)
* Maintained **foreign key relationship** with `restaurant_id`

Output:

```
data/processed/orders_cleaned.csv
```

Acts as **Fact Table (Historical)**

---

### 3️⃣ Real-Time Data Simulation (Kafka)

* Kafka used to simulate live order events
* Python producer streams data from `orders_cleaned.csv`

---

### 4️⃣ Stream Processing (PySpark)

* Consumes Kafka stream
* Parses JSON data
* Joins with restaurant dataset
* Performs transformations

---

### 5️⃣ Data Storage

#### 🪣 Data Lake

* Format: Parquet
* Benefits:

  * Columnar storage
  * Fast queries
  * Scalable

#### PostgreSQL

* Structured storage
* Used for BI queries

---

### 6️⃣ Visualization

* Power BI connected to PostgreSQL
* Dashboards include:

  * Revenue trends
  * Order distribution
  * Restaurant performance
  * Delivery metrics

---

## ▶️ How to Run the Project

---

### Step 1: Start Kafka (Docker)

```bash
docker compose up -d
```

Check containers:

```bash
docker ps
```

---

### Step 2: Create Kafka Topic

```bash
docker exec -it kafka-kraft kafka-topics.sh --create \
--topic food_orders \
--bootstrap-server localhost:9092 \
--partitions 1 \
--replication-factor 1
```

---

### Step 3: Test Kafka (Optional)

Producer:

```bash
docker exec -it kafka-kraft kafka-console-producer.sh \
--topic food_orders \
--bootstrap-server localhost:9092
```

Consumer:

```bash
docker exec -it kafka-kraft kafka-console-consumer.sh \
--topic food_orders \
--from-beginning \
--bootstrap-server localhost:9092
```

---

### Step 4: Run Kafka Producer Script

```bash
python producer.py
```

---

### Step 5: Start PySpark (Docker)

```bash
docker run -it --rm --network=host \
-v "C:/DE project:/app" \
-u root apache/spark:3.5.0 /bin/bash
```

---

### Step 6: Setup Environment (Inside Container)

```bash
mkdir -p /tmp/.ivy2/cache /tmp/.ivy2/jars
export HOME=/tmp
```

---

### Step 7: Run Batch Job

```bash
/opt/spark/bin/spark-submit \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
--conf spark.jars.ivy=/tmp/.ivy2 \
/app/spark/load_historical_data.py
```

---

### Step 8: Run Streaming Job

```bash
/opt/spark/bin/spark-submit \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
--conf spark.jars.ivy=/tmp/.ivy2 \
/app/spark/streaming_job.py
```

---

## Dashboard
<img width="1358" height="719" alt="image" src="https://github.com/user-attachments/assets/3c65c495-c8fa-4a15-ac7c-774f3aa91d4d" />

---

## Key Concepts Demonstrated

* Data Cleaning & EDA
* Synthetic Data Generation
* Kafka Streaming Architecture
* PySpark Structured Streaming
* Fact-Dimension Modeling (Star Schema)
* Data Lake (Parquet)
* OLAP Database Integration
* Real-Time Analytics

---

## Why This Project Matters

This project replicates a **real-world data engineering system**:

* Handles both **batch and streaming data**
* Uses **scalable distributed processing**
* Demonstrates **end-to-end pipeline design**
* Integrates **analytics + visualization**

---


## Author

Sharvari Gupte
(Data Science & Data Engineering Enthusiast)

---
