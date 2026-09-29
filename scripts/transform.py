import os
import glob
import pandas as pd
from datetime import datetime

def transform_crypto_data():
    # Setting the paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bronze_dir = os.path.abspath(os.path.join(base_dir, "../data/bronze"))
    silver_dir = os.path.abspath(os.path.join(base_dir, "../data/silver"))
    
    # Creating a silver file if not exists
    os.makedirs(silver_dir, exist_ok=True)
    
    # Searching for all the JSON files inside the bronze folder
    json_files = glob.glob(os.path.join(bronze_dir, "*.json"))
    
    if not json_files:
        raise FileNotFoundError("No JSON files found in the Bronze layer!")
        
    # Selectiong the last on file 
    latest_file = max(json_files, key=os.path.getmtime)
    print(f"Reading unprocessed data from: {latest_file}")

    # Loading data to Pandas DataFrame
    df = pd.read_json(latest_file)
    
    # Transformation and cleaning
    target_columns = ["id", "symbol", "name", "current_price", "market_cap", "total_volume", "price_change_percentage_24h"]
    
    # Checking if there are columns before filtering them 
    existing_cols = [col for col in target_columns if col in df.columns]
    df_clean = df[existing_cols].copy()
    
    # Renaming of the columns for cleaner form or addition of metadata
    df_clean["transformed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Saving to the silver layer with unique name (CSV)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = os.path.join(silver_dir, f"coingecko_silver_{timestamp}.parquet")
    
    df_clean.to_parquet(file_path, index=False)
    print(f"Data successfully transformed and saved as Parquet to {file_path}")

if __name__ == "__main__":
    transform_crypto_data()