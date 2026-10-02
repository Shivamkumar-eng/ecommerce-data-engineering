from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, countDistinct

# Start Spark
spark = (
    SparkSession.builder
    .appName("EcommerceSilverToGold")
    .master("local[*]")
    .getOrCreate()
)

SILVER_PATH = "/opt/spark-data/silver"
GOLD_PATH = "/opt/spark-data/gold"


# =========================
# READ SILVER DATA
# =========================

customers = spark.read.parquet(
    f"{SILVER_PATH}/customers"
)

products = spark.read.parquet(
    f"{SILVER_PATH}/products"
)

orders = spark.read.parquet(
    f"{SILVER_PATH}/orders"
)

payments = spark.read.parquet(
    f"{SILVER_PATH}/payments"
)

print("\n========== SILVER DATA LOADED ==========")

print("Customers:", customers.count())
print("Products:", products.count())
print("Orders:", orders.count())
print("Payments:", payments.count())


# =========================
# CALCULATE ORDER REVENUE
# =========================

orders_with_products = orders.join(
    products.select("product_id", "price"),
    on="product_id",
    how="left"
)

orders_with_products = orders_with_products.withColumn(
    "revenue",
    col("quantity") * col("price")
)

print("\n========== ORDER REVENUE CALCULATED ==========")

orders_with_products.select(
    "order_id",
    "product_id",
    "quantity",
    "price",
    "revenue"
).show(10)


# =========================
# GOLD 1: CUSTOMER REVENUE
# =========================

customer_revenue = (
    orders_with_products
    .groupBy("customer_id")
    .agg(
        countDistinct("order_id").alias("total_orders"),
        sum("revenue").alias("total_revenue")
    )
)

customer_revenue.write.mode("overwrite").parquet(
    f"{GOLD_PATH}/customer_revenue"
)

print("Customer Revenue Gold completed.")


# =========================
# GOLD 2: PRODUCT SALES
# =========================

product_sales = (
    orders_with_products
    .groupBy("product_id")
    .agg(
        count("order_id").alias("total_orders"),
        sum("quantity").alias("units_sold"),
        sum("revenue").alias("total_revenue")
    )
)

product_sales.write.mode("overwrite").parquet(
    f"{GOLD_PATH}/product_sales"
)

print("Product Sales Gold completed.")


# =========================
# GOLD 3: DAILY SALES
# =========================

daily_sales = (
    orders_with_products
    .groupBy("order_date")
    .agg(
        countDistinct("order_id").alias("total_orders"),
        sum("revenue").alias("total_revenue")
    )
)

daily_sales.write.mode("overwrite").parquet(
    f"{GOLD_PATH}/daily_sales"
)

print("Daily Sales Gold completed.")


# =========================
# GOLD 4: PAYMENT SUMMARY
# =========================

payment_summary = (
    payments
    .groupBy("payment_method")
    .agg(
        count("payment_id").alias("total_payments")
    )
)

payment_summary.write.mode("overwrite").parquet(
    f"{GOLD_PATH}/payment_summary"
)

print("Payment Summary Gold completed.")


print("\n========== SILVER → GOLD COMPLETED ==========")

spark.stop()