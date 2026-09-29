import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, "../.env")
load_dotenv(dotenv_path=env_path)

# Database connection (using 'postgres' for Docker)
DB_CONN = os.getenv("DATABASE_URL", "postgresql+psycopg2://airflow:airflow@postgres/airflow")

def run_quality_checks():
    print("Starting Data Quality Checks on PostgreSQL...")
    engine = create_engine(DB_CONN)
    
    with engine.connect() as connection:
        
        # Check: Does the table contain any data?
        result = connection.execute(text("SELECT COUNT(*) FROM crypto_prices;"))
        row_count = result.scalar()
        print(f"-> Row Count Check: Found {row_count} rows.")
        if row_count == 0:
            raise AssertionError("Data Quality Error: The 'crypto_prices' table is empty!")

        # Check: Are there any NULL values in the names?
        result = connection.execute(text("SELECT COUNT(*) FROM crypto_prices WHERE name IS NULL;"))
        null_names = result.scalar()
        print(f"-> NULL Name Check: Found {null_names} NULL values.")
        if null_names > 0:
            raise AssertionError("Data Quality Error: Found cryptocurrencies without a name (NULL)!")

        # Check: Are all price values positive numbers?
        result = connection.execute(text("SELECT COUNT(*) FROM crypto_prices WHERE current_price <= 0;"))
        invalid_prices = result.scalar()
        print(f"-> Price Validity Check: Found {invalid_prices} invalid prices.")
        if invalid_prices > 0:
            raise AssertionError("Data Quality Error: Found zero or negative cryptocurrency prices!")

    print("All Data Quality Checks completed successfully!")

if __name__ == "__main__":
    run_quality_checks()
