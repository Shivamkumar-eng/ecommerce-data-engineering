from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("CheckProduct1088Bronze")
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

print("\n========== PRODUCT 1088 IN BRONZE PRODUCTS ==========")

products.filter(
    col("product_id") == 1088
).show(truncate=False)

print("\n========== ORDERS FOR PRODUCT 1088 ==========")

orders.filter(
    col("product_id") == 1088
).show(20, truncate=False)

print("\n========== COUNTS ==========")

print(
    "Product 1088 in products:",
    products.filter(col("product_id") == 1088).count()
)

print(
    "Orders containing product 1088:",
    orders.filter(col("product_id") == 1088).count()
)

spark.stop()