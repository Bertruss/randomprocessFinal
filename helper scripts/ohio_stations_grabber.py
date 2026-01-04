import requests
import json
import pandas as pd
import time
from datetime import datetime as dt
with open("../token.txt", "r") as file:
    token = file.readline()
headers = {"token": token}


# pull all stations in the state of ohio
stations_req = "https://www.ncei.noaa.gov/cdo-web/api/v2/stations"
offset = 1
delay = 2
all_rows = []
data = []
while True:
    params = {
        "locationid": "FIPS:39",
        "limit": 1000,
        "offset": offset
    }

    req = requests.get(stations_req, headers=headers, params=params)
    print("STATUS:", req.status_code)
    rcount = 0
    while not (req.status_code == 200) and rcount < 20:
        # retry
        rcount += 1
        print("retrying ...")
        time.sleep(5 + rcount)
        req = requests.get(stations_req, headers=headers, params=params)
        print("STATUS:", req.status_code)
    data = req.json()
    if "results" not in data:
        break

    all_rows.extend(data["results"])
    offset += 1000
    time.sleep(delay)

breakpoint()
"""
print(start_date.isoformat())
breakpoint()

buffer = BytesIO()
url = f"https://api.weather.gov/stations/{station}/observations"

c = pycurl.Curl()
c.setopt(c.URL, url)
"""