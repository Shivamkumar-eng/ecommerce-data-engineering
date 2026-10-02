import pandas as pd
import random
from faker import Faker

fake = Faker()

# -------------------------
# Configuration
# -------------------------

NUM_CUSTOMERS = 10000
NUM_PRODUCTS = 1000
NUM_ORDERS = 50000
NUM_PAYMENTS = 50000


# -------------------------
# 1. Generate Customers
# -------------------------

customers = []

for customer_id in range(1, NUM_CUSTOMERS + 1):

    email = fake.email()
    city = fake.city()

    # Introduce missing emails (~2%)
    if random.random() < 0.02:
        email = None

    # Introduce inconsistent city formatting (~3%)
    if random.random() < 0.03:
        city = city.lower()

    customers.append({
        "customer_id": customer_id,
        "name": fake.name(),
        "email": email,
        "city": city,
        "state": fake.state(),
        "age": random.randint(18, 70)
    })

customers_df = pd.DataFrame(customers)

# Add duplicate customer records (~1%)
duplicate_customers = customers_df.sample(
    frac=0.01,
    random_state=42
)

customers_df = pd.concat(
    [customers_df, duplicate_customers],
    ignore_index=True
)


# -------------------------
# 2. Generate Products
# -------------------------

categories = [
    "Electronics",
    "Clothing",
    "Home",
    "Books",
    "Sports"
]

products = []

for product_id in range(1, NUM_PRODUCTS + 1):

    category = random.choice(categories)
    price = round(random.uniform(100, 100000), 2)

    # Missing category (~2%)
    if random.random() < 0.02:
        category = None

    # Invalid negative price (~1%)
    if random.random() < 0.01:
        price = -price

    products.append({
        "product_id": product_id,
        "product_name": fake.word().capitalize(),
        "category": category,
        "price": price
    })

products_df = pd.DataFrame(products)


# -------------------------
# 3. Generate Orders
# -------------------------

orders = []

for order_id in range(1, NUM_ORDERS + 1):

    customer_id = random.randint(1, NUM_CUSTOMERS)
    product_id = random.randint(1, NUM_PRODUCTS)
    quantity = random.randint(1, 5)

    # Invalid customer ID (~1%)
    if random.random() < 0.01:
        customer_id = random.randint(
            NUM_CUSTOMERS + 1,
            NUM_CUSTOMERS + 1000
        )

    # Invalid product ID (~1%)
    if random.random() < 0.01:
        product_id = random.randint(
            NUM_PRODUCTS + 1,
            NUM_PRODUCTS + 100
        )

    # Invalid quantity (~1%)
    if random.random() < 0.01:
        quantity = 0

    orders.append({
        "order_id": order_id,
        "customer_id": customer_id,
        "product_id": product_id,
        "quantity": quantity,
        "order_date": fake.date_between(
            start_date="-1y",
            end_date="today"
        )
    })

orders_df = pd.DataFrame(orders)


# -------------------------
# 4. Generate Payments
# -------------------------

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Cash"
]

payments = []

for payment_id in range(1, NUM_PAYMENTS + 1):

    payment_method = random.choice(payment_methods)

    # Missing payment method (~2%)
    if random.random() < 0.02:
        payment_method = None

    # Inconsistent status values
    payment_status = random.choice([
        "Success",
        "Success",
        "Success",
        "Failed",
        "success",
        "FAILED"
    ])

    payments.append({
        "payment_id": payment_id,
        "order_id": payment_id,
        "payment_method": payment_method,
        "payment_status": payment_status
    })

payments_df = pd.DataFrame(payments)


# -------------------------
# 5. Save Raw Data
# -------------------------

customers_df.to_csv(
    "data/raw/customers.csv",
    index=False
)

products_df.to_csv(
    "data/raw/products.csv",
    index=False
)

orders_df.to_csv(
    "data/raw/orders.csv",
    index=False
)

payments_df.to_csv(
    "data/raw/payments.csv",
    index=False
)


# -------------------------
# Summary
# -------------------------

print("Raw data generation completed!")
print(f"Customers: {len(customers_df)}")
print(f"Products: {len(products_df)}")
print(f"Orders: {len(orders_df)}")
print(f"Payments: {len(payments_df)}")
print("\nNote: Intentional data quality issues were introduced.")