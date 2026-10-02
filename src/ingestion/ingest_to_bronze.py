import shutil
from pathlib import Path

RAW_PATH = Path("data/raw")
BRONZE_PATH = Path("data/bronze")

BRONZE_PATH.mkdir(parents=True, exist_ok=True)


def ingest_file(filename):
    source_file = RAW_PATH / filename
    destination_file = BRONZE_PATH / filename

    shutil.copy2(source_file, destination_file)

    print(f"Ingested {filename}")


def main():

    files = [
        "customers.csv",
        "products.csv",
        "orders.csv",
        "payments.csv"
    ]

    for file in files:
        ingest_file(file)

    print("\nBronze ingestion completed successfully!")


if __name__ == "__main__":
    main()