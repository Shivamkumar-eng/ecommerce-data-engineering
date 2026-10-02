from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, lower, when


# ============================================================
# SPARK SESSION
# ============================================================

spark = (
    SparkSession.builder
    .appName("EcommerceBronzeToSilver")
    .master("local[*]")
    .getOrCreate()
)


# ============================================================
# PATHS
# ============================================================

BRONZE_PATH = "/opt/spark-data/bronze"
SILVER_PATH = "/opt/spark-data/silver"
QUARANTINE_PATH = "/opt/spark-data/quarantine"


# ============================================================
# READ BRONZE DATA
# ============================================================

customers = spark.read.csv(
    f"{BRONZE_PATH}/customers.csv",
    header=True,
    inferSchema=True
)

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

payments = spark.read.csv(
    f"{BRONZE_PATH}/payments.csv",
    header=True,
    inferSchema=True
)


# ============================================================
# CUSTOMERS
# ============================================================

print("\n========== CUSTOMERS ==========")

customers_deduplicated = customers.dropDuplicates(
    ["customer_id"]
)

print(
    "Customers before duplicates:",
    customers.count()
)

print(
    "Customers after duplicates:",
    customers_deduplicated.count()
)


# ------------------------------------------------------------
# CUSTOMER EMAIL VALIDATION
# ------------------------------------------------------------

invalid_customers = customers_deduplicated.filter(
    col("email").isNull()
)

valid_customers = customers_deduplicated.filter(
    col("email").isNotNull()
)

print(
    "Customers with missing emails:",
    invalid_customers.count()
)

print(
    "Valid customers:",
    valid_customers.count()
)


# ------------------------------------------------------------
# CUSTOMER NORMALIZATION
# ------------------------------------------------------------

customers_silver = valid_customers.withColumn(
    "city",
    trim(lower(col("city")))
)


# ------------------------------------------------------------
# WRITE CUSTOMER SILVER
# ------------------------------------------------------------

customers_silver.write.mode("overwrite").parquet(
    f"{SILVER_PATH}/customers"
)


# ------------------------------------------------------------
# QUARANTINE INVALID CUSTOMERS
# ------------------------------------------------------------

invalid_customers.write.mode("overwrite").parquet(
    f"{QUARANTINE_PATH}/customers"
)

print("Customers Silver + Quarantine completed.")


# ============================================================
# PRODUCTS
# ============================================================

print("\n========== PRODUCTS ==========")

products_deduplicated = products.dropDuplicates(
    ["product_id"]
)

print(
    "Products before duplicates:",
    products.count()
)

print(
    "Products after duplicates:",
    products_deduplicated.count()
)


# ------------------------------------------------------------
# WRITE PRODUCT SILVER
# ------------------------------------------------------------

products_deduplicated.write.mode("overwrite").parquet(
    f"{SILVER_PATH}/products"
)

print("Products Silver completed.")


# ============================================================
# ORDERS
# ============================================================

print("\n========== ORDERS ==========")

orders_deduplicated = orders.dropDuplicates(
    ["order_id"]
)

print(
    "Orders before duplicates:",
    orders.count()
)

print(
    "Orders after duplicates:",
    orders_deduplicated.count()
)


# ------------------------------------------------------------
# PRODUCT REFERENTIAL INTEGRITY
# ------------------------------------------------------------

product_ids = products.select(
    "product_id"
).distinct()


# Orders whose product_id does not exist
# in the product master table
orphan_orders = orders_deduplicated.join(
    product_ids,
    on="product_id",
    how="left_anti"
)


# Orders whose product_id exists
# in the product master table
valid_orders = orders_deduplicated.join(
    product_ids,
    on="product_id",
    how="left_semi"
)


print(
    "Orphan orders:",
    orphan_orders.count()
)

print(
    "Valid orders:",
    valid_orders.count()
)


# ------------------------------------------------------------
# WRITE VALID ORDERS TO SILVER
# ------------------------------------------------------------

valid_orders.write.mode("overwrite").parquet(
    f"{SILVER_PATH}/orders"
)


# ------------------------------------------------------------
# QUARANTINE ORPHAN ORDERS
# ------------------------------------------------------------

orphan_orders.write.mode("overwrite").parquet(
    f"{QUARANTINE_PATH}/orders"
)

print("Orders Silver + Quarantine completed.")


# ============================================================
# PAYMENTS
# ============================================================

print("\n========== PAYMENTS ==========")

payments_deduplicated = payments.dropDuplicates(
    ["payment_id"]
)

print(
    "Payments before duplicates:",
    payments.count()
)

print(
    "Payments after duplicates:",
    payments_deduplicated.count()
)


# ------------------------------------------------------------
# PAYMENT QUALITY FLAG
# ------------------------------------------------------------

payments_silver = payments_deduplicated.withColumn(
    "payment_quality",
    when(
        col("payment_method").isNull(),
        "missing_payment_method"
    ).otherwise(
        "valid"
    )
)


print(
    "Payments with missing method:",
    payments_silver.filter(
        col("payment_method").isNull()
    ).count()
)


print(
    "Valid payment records:",
    payments_silver.filter(
        col("payment_quality") == "valid"
    ).count()
)


# ------------------------------------------------------------
# WRITE PAYMENT SILVER
# ------------------------------------------------------------

payments_silver.write.mode("overwrite").parquet(
    f"{SILVER_PATH}/payments"
)

print("Payments Silver completed.")


# ============================================================
# PIPELINE COMPLETED
# ============================================================

print("\n========== PIPELINE COMPLETED ==========")

spark.stop()