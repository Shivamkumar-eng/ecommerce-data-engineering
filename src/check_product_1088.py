from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("CheckProduct1088")
    .master("local[*]")
    .getOrCreate()
)

SILVER_PATH = "/opt/spark-data/silver"

products = spark.read.parquet(
    f"{SILVER_PATH}/products"
)

print("\n========== PRODUCT 1088 ==========")

products.filter(
    col("product_id") == 1088
).show(truncate=False)

print("\n========== PRODUCTS WITH NULL PRICE ==========")

products.filter(
    col("price").isNull()
).show(20, truncate=False)

print("\n========== NULL PRICE COUNT ==========")

print(
    "Count:",
    products.filter(
        col("price").isNull()
    ).count()
)

spark.stop()