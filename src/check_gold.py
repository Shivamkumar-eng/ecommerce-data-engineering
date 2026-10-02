from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("CheckGoldData")
    .master("local[*]")
    .getOrCreate()
)

GOLD_PATH = "/opt/spark-data/gold"

customer_revenue = spark.read.parquet(
    f"{GOLD_PATH}/customer_revenue"
)

product_sales = spark.read.parquet(
    f"{GOLD_PATH}/product_sales"
)

daily_sales = spark.read.parquet(
    f"{GOLD_PATH}/daily_sales"
)

payment_summary = spark.read.parquet(
    f"{GOLD_PATH}/payment_summary"
)

print("\n========== CUSTOMER REVENUE ==========")
customer_revenue.show(10, truncate=False)

print("\n========== PRODUCT SALES ==========")
product_sales.show(10, truncate=False)

print("\n========== DAILY SALES ==========")
daily_sales.show(10, truncate=False)

print("\n========== PAYMENT SUMMARY ==========")
payment_summary.show(truncate=False)

spark.stop()