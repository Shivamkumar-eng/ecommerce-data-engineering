from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("EcommerceDataPipeline") \
    .getOrCreate()

print("Spark Version:", spark.version)

spark.stop()