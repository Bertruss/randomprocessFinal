import requests
import json
import pandas as pd
from datetime import datetime as dt
import time

with open("tokenNEI.txt", "r") as file:
    token = file.readline()
headers = {"api_key": token}

all_rows = pd.DataFrame()
url = "https://api.eia.gov/v2/electricity/electric-power-operational-data/data/"
delay = 1
offset = 1
total = 0
breakpoint()
while True:
    print(offset)
    params = {
        "api_key": token,
        "frequency": "monthly",
        "data[0]": "cost",
        "data[1]": "cost-per-btu",
        "data[2]": "generation",
        "data[3]": "heat-content",
        "data[4]": "total-consumption",
        "facets[location][]": "OH",
        "start": "2001-01",
        "end": "2025-09",
        "offset": offset,
        "length": 5000
    }
    req = requests.get(url, headers=headers, params=params)
    print("STATUS:", req.status_code)
    rcount = 0
    while not (req.status_code == 200) and rcount < 20:
        # retry
        rcount += 1
        print("retrying ...")
        time.sleep(1 + rcount)
        req = requests.get(url, headers=headers, params=params)
        print("STATUS:", req.status_code)
    data = req.json()

    if total == 0:
        total = int(data["response"]["total"])    
    
    if  total < offset:
        breakpoint()

    if "response" not in data:
        break
    all_rows = pd.concat([all_rows, pd.DataFrame(data["response"]["data"])], ignore_index=True)
    offset += 5000
    time.sleep(delay)
    
breakpoint()