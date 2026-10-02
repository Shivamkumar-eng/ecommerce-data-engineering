from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("CheckSilverSchema")
    .master("local[*]")
    .getOrCreate()
)

orders = spark.read.parquet(
    "/opt/spark-data/silver/orders"
)

payments = spark.read.parquet(
    "/opt/spark-data/silver/payments"
)

print("\n========== ORDERS SCHEMA ==========")
orders.printSchema()

print("\n========== PAYMENTS SCHEMA ==========")
payments.printSchema()

spark.stop()