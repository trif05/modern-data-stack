import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def fetch_crypto_data():
    url="https://api.coingecko.com/api/v3/coins/markets"
    api_key = os.getenv("COINGECKO_API_KEY")
    params={
        "vs_currency" : "usd", # Reference currency.
        "order" : "market_cap_desc", # Shorting per capitalization.
        "per_page" : 10, # Top 10(first 10) coins.
        "page" : 1, # First page.
        "sparkline" : "false", # No graphs.
        "x_cg_demo_api_key" : api_key # My API key.
    }

    headers={
        "accept" : "application/json" # When reply give me JSON data.
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data=response.json()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        bronze_dir = os.path.abspath(os.path.join(base_dir, "../data/bronze"))

        os.makedirs(bronze_dir, exist_ok=True) # Bronze forlder creation if not exists
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # Saving by unique name based on datetime.
        file_path = f"{bronze_dir}/coingecko_raw_{timestamp}.json"

        with open(file_path, "w", encoding="utf-8") as f:
            # Json file format
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data successfully fetched and saved to {file_path}")
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")
    
if __name__ == "__main__":
    fetch_crypto_data()