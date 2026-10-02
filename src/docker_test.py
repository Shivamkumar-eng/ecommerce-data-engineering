from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("DockerParquetTest") \
    .master("local[*]") \
    .getOrCreate()

df = spark.range(5)

print("Row count:", df.count())

df.write.mode("overwrite").parquet("/opt/spark-data/test_parquet")

print("PARQUET WRITE SUCCESS")

spark.stop()
