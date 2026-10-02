from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("CheckPaymentQuality")
    .master("local[*]")
    .getOrCreate()
)

BRONZE_PATH = "/opt/spark-data/bronze"
SILVER_PATH = "/opt/spark-data/silver"

# Read Bronze and Silver payments
bronze_payments = spark.read.csv(
    f"{BRONZE_PATH}/payments.csv",
    header=True,
    inferSchema=True
)

silver_payments = spark.read.parquet(
    f"{SILVER_PATH}/payments"
)

print("\n========== BRONZE PAYMENTS ==========")

print(
    "Bronze payments:",
    bronze_payments.count()
)

print(
    "Bronze duplicate payment IDs:",
    bronze_payments.count()
    - bronze_payments.dropDuplicates(["payment_id"]).count()
)

print(
    "Bronze NULL payment methods:",
    bronze_payments.filter(
        col("payment_method").isNull()
    ).count()
)


print("\n========== SILVER PAYMENTS ==========")

print(
    "Silver payments:",
    silver_payments.count()
)

print(
    "Silver duplicate payment IDs:",
    silver_payments.count()
    - silver_payments.dropDuplicates(["payment_id"]).count()
)

print(
    "Silver NULL payment methods:",
    silver_payments.filter(
        col("payment_method").isNull()
    ).count()
)


print("\n========== SAMPLE NULL PAYMENT METHODS ==========")

bronze_payments.filter(
    col("payment_method").isNull()
).show(10, truncate=False)


print("\n========== NULL METHOD ORDER MATCH ==========")

null_method_payments = bronze_payments.filter(
    col("payment_method").isNull()
)

orders = spark.read.parquet(
    f"{SILVER_PATH}/orders"
)

matched_payments = null_method_payments.join(
    orders.select("order_id"),
    on="order_id",
    how="inner"
)

unmatched_payments = null_method_payments.join(
    orders.select("order_id"),
    on="order_id",
    how="left_anti"
)

print(
    "NULL-method payments:",
    null_method_payments.count()
)

print(
    "NULL-method payments with matching orders:",
    matched_payments.count()
)

print(
    "NULL-method payments without matching orders:",
    unmatched_payments.count()
)



print("\n========== UNMATCHED PAYMENT CHECK ==========")

unmatched_payments.select(
    "payment_id",
    "order_id",
    "payment_method",
    "payment_status"
).show(20, truncate=False)

print("\n========== UNMATCHED PAYMENT ORDER IDS ==========")

unmatched_payments.select(
    "order_id"
).show(20, truncate=False)



print("\n========== UNMATCHED PAYMENTS vs BRONZE ORDERS ==========")

bronze_orders = spark.read.csv(
    f"{BRONZE_PATH}/orders.csv",
    header=True,
    inferSchema=True
)

unmatched_with_orders = unmatched_payments.join(
    bronze_orders.select(
        "order_id",
        "product_id"
    ),
    on="order_id",
    how="left"
)

unmatched_with_orders.select(
    "payment_id",
    "order_id",
    "product_id",
    "payment_method",
    "payment_status"
).show(20, truncate=False)


spark.stop()