from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("CheckNullProduct")
    .master("local[*]")
    .getOrCreate()
)

GOLD_PATH = "/opt/spark-data/gold"

product_sales = spark.read.parquet(
    f"{GOLD_PATH}/product_sales"
)

print("\n========== PRODUCTS WITH NULL REVENUE ==========")

product_sales.filter(
    col("total_revenue").isNull()
).show(truncate=False)

print("\n========== PRODUCTS WITH NULL REVENUE COUNT ==========")

print(
    "Count:",
    product_sales.filter(
        col("total_revenue").isNull()
    ).count()
)

spark.stop()