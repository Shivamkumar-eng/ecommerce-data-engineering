# 🛒 E-Commerce Data Engineering Pipeline

A production-style **E-Commerce Data Engineering pipeline** built using **Apache Spark, Python, Docker, and Parquet**.

The project demonstrates how raw e-commerce data can be transformed through a **Bronze → Silver → Gold architecture**, with data cleaning, deduplication, validation, referential-integrity checks, quarantine handling, and analytical aggregations.

---

## 📌 Project Overview

This project simulates an e-commerce data platform containing:

- Customers
- Products
- Orders
- Payments

The pipeline processes raw CSV data through multiple layers:

```text
Raw CSV Data
     │
     ▼
┌─────────────┐
│   BRONZE    │
│ Raw Data    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   SILVER    │
│ Cleaned &   │
│ Validated   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    GOLD     │
│ Analytics & │
│ Aggregates  │
└─────────────┘


🏗️ Architecture

![alt text](<E-Commerce Data Engineering Pipeline-1.png>)

Bronze Layer

The Bronze layer contains the original CSV datasets.

data/bronze/
├── customers.csv
├── products.csv
├── orders.csv
└── payments.csv

The raw data is intentionally designed to contain data-quality issues such as:

Duplicate customer/order/payment records
Missing customer emails
Missing payment methods
Orders referencing non-existent products
🧹 Silver Layer

The Silver layer performs data cleaning and validation using Apache Spark.

Customers

Operations performed:

Deduplication using customer_id
Detection of missing emails
Valid customer records written to Silver
Invalid records moved to quarantine
City values normalized using lowercase and trimming
Products

Operations performed:

Deduplication using product_id
Clean product records written to Silver
Orders

Orders are validated against the product master.

A left anti join identifies orders whose product_id does not exist in the product table.

These records are moved to quarantine.

Bronze Orders
      │
      ├── Valid Product ID ──────► Silver Orders
      │
      └── Invalid Product ID ────► Quarantine
Payments

Payment records are deduplicated using payment_id.

Missing payment methods are identified using a payment_quality column.

payment_method IS NULL
        │
        ▼
missing_payment_method

The original records are preserved rather than silently modifying the source data.

🚨 Quarantine

Invalid records are separated from valid Silver data instead of being discarded.

data/quarantine/
├── customers/
└── orders/

This provides traceability for rejected records and prevents invalid records from entering downstream analytical tables.

📊 Data Quality Results

The pipeline produced the following results.

Dataset	Result
Bronze Customers	10,000+
Valid Silver Customers	9,784
Bronze Products	1,000
Valid Silver Products	1,000
Bronze Orders	50,000
Valid Silver Orders	49,492
Quarantined Orders	508
Bronze Payments	50,000
Payments with Missing Method	1,076
Order reconciliation
50,000 Bronze Orders
        │
        ├── 49,492 Valid Orders
        │
        └── 508 Quarantined Orders

49,492 + 508 = 50,000

The 508 quarantined orders were caused by references to product IDs that were not present in the product master.

🥇 Gold Layer

The Gold layer contains analytical datasets generated from validated Silver data.

Customer Revenue
customer_revenue

Contains:

customer_id
total_orders
total_revenue
Product Sales
product_sales

Contains:

product_id
total_orders
units_sold
total_revenue
Daily Sales
daily_sales

Contains:

order_date
total_orders
total_revenue
Payment Summary
payment_summary

Contains:

payment_method
total_payments

The payment summary also retains the NULL payment-method category so that the original data-quality issue remains visible.

🔍 Data Quality Checks

The project includes validation scripts for checking pipeline results.

Examples include:

Payment data quality
Orphan orders
Gold-layer validation
Product revenue validation
Schema checks

Important validation performed:

Referential Integrity

Orders are checked against the product master before entering Silver.

Duplicate Detection

Duplicate IDs are checked before downstream processing.

Missing Values

Important missing values such as:

Customer email
Payment method

are explicitly identified.

Revenue Validation

Gold product-sales data is checked to ensure that valid product records do not produce unexpected NULL revenue values.

🛠️ Tech Stack
Programming
Python
Data Engineering
Apache Spark
PySpark
SQL
Parquet
Infrastructure
Docker
Docker Compose
Development
VS Code
Git
GitHub
🐳 Docker Setup

The Spark environment runs inside Docker using:

Apache Spark 3.5.8
Python
Java

Docker is used to provide a Linux-based Spark environment and avoid Windows-specific Hadoop native library issues during Parquet processing.

📁 Project Structure
project/
│
├── docker-compose.yml
├── README.md
│
├── data/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── quarantine/
│
├── notebooks/
│   └── 01_data_exploration.ipynb
│
├── sql/
│
└── src/
    ├── generate_data.py
    ├── docker_test.py
    ├── check_payment_quality.py
    │
    ├── ingestion/
    │
    ├── quality/
    │
    └── transformations/
        ├── bronze_to_silver.py
        ├── bronze_to_silver_backup.py
        ├── silver_to_gold.py
        └── test_spark.py

