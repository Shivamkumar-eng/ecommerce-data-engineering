from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("CheckOrphanProducts")
    .master("local[*]")
    .getOrCreate()
)

BRONZE_PATH = "/opt/spark-data/bronze"

products = spark.read.csv(
    f"{BRONZE_PATH}/products.csv",
    header=True,
    inferSchema=True
)

orders = spark.read.csv(
    f"{BRONZE_PATH}/orders.csv",
    header=True,
    inferSchema=True
)

# Get unique product IDs from the product master
product_ids = products.select(
    "product_id"
).distinct()

# Find orders whose product_id doesn't exist in products
orphan_orders = orders.join(
    product_ids,
    on="product_id",
    how="left_anti"
)

print("\n========== ORPHAN ORDERS ==========")

orphan_orders.show(20, truncate=False)

print("\n========== ORPHAN ORDER COUNT ==========")

print(
    "Orphan orders:",
    orphan_orders.count()
)

print("\n========== ORPHAN PRODUCT IDs ==========")

orphan_product_ids = orphan_orders.select(
    "product_id"
).distinct()

orphan_product_ids.show(100, truncate=False)

print("\n========== ORPHAN PRODUCT ID COUNT ==========")

print(
    "Orphan product IDs:",
    orphan_product_ids.count()
)

spark.stop()