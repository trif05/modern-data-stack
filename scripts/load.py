import os
import pandas as pd
import glob
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv() # Loading the .env 

DB_CONN = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://airflow:airflow@postgres/airflow"
)

def create_db_engine():
    try:
        engine = create_engine(DB_CONN)
        print("Successfully connected to the PostgreSQL database!")
        return engine
    except Exception as e:
        print(f"Error connecting to the database:{e}")
        raise e
    

def load_silver_to_postgres(engine):
    """Reading the latest Parquet file from silver layer and save it to the PostgreSQL"""
    # Searching for the parquet file inside the folder data/silver
    silver_dir = "data/silver"
    parquet_files = glob.glob(os.path.join(silver_dir, "*.parquet"))
    
    if not parquet_files:
        print("No Parquet files were found in the Silver layer!")
        return

    # We select the most recent file based on creation time.
    latest_file = max(parquet_files, key=os.path.getmtime)
    print(f"File found for loading: {latest_file}")

    try:
        # Reading parquet file to pandas dataframe
        df = pd.read_parquet(latest_file)
        print(f"DataFrame loaded succesfully with {len(df)} lines.")

        # Loading data to the PostgreSQL
        table_name = "crypto_prices"
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='append',
            index=False 
        )
        print(f"Data successfully loaded into the table.'{table_name}'")

    except Exception as e:
        print(f"Error while loading the file: {e}")
        raise e

if __name__ == "__main__":
    db_engine = create_db_engine()
    load_silver_to_postgres(db_engine)