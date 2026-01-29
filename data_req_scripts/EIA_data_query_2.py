import requests
import json
import pandas as pd
from datetime import datetime as dt
import time

with open("tokenNEI.txt", "r") as file:
    token = file.readline()
headers = {"api_key": token}

API_KEY = token
STATE = "OH"
SECTORS = ["RES", "COM"]  # Residential, Commercial
BASE_URL = "https://api.eia.gov/v2/electricity/retail-sales/data"

# Columns to request
DATA_COLS = ["price", "sales"]  # price = avg retail price (¢/kWh), sales = MWh sold

# Common parametersc
common_params = {
    "api_key": API_KEY,
    "frequency": "monthly",
    "facets[stateid][]": STATE,
    "start": "1990-01",    # earliest possible
    "end": "2025-11",      # latest you asked about
}

# Store data for each sector
dfs = []
for sector in SECTORS:
    params = {
        **common_params,
        "facets[sectorid][]": sector,
    }
    # Add requested columns
    for col in DATA_COLS:
        params[f"data[]"] = col

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    data = response.json().get("response", {}).get("data", [])

    # Turn into DataFrame
    df = pd.DataFrame(data)
    if df.empty:
        print(f"No data returned for sector {sector}.")
        continue

    # Convert period to DateTime
    df["period"] = pd.to_datetime(df["period"], format="%Y-%m")
    df.set_index("period", inplace=True)
    df["sector"] = sector
    dfs.append(df)

# Combine into one DataFrame
result = pd.concat(dfs)

print(result.head())

# Save to CSV
result.to_csv("ohio_retail_sales_price.csv")
print("Saved to ohio_retail_sales_price.csv")


breakpoint()