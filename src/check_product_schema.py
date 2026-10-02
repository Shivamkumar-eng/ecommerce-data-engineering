from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("CheckProductSchema")
    .master("local[*]")
    .getOrCreate()
)

products = spark.read.parquet(
    "/opt/spark-data/silver/products"
)

print("\n========== PRODUCTS SCHEMA ==========")
products.printSchema()

spark.stop()