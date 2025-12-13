import requests
import json
import pandas as pd
from datetime import datetime as dt
import time

with open("token.txt", "r") as file:
    token = file.readline()
headers = {"token": token}

breakpoint()
start_year = 1990
end_year = 2025

## load list of stations
station_list = pd.read_csv("observation_station_list.csv")

url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"
delay = 2

for index, station in station_list.iterrows():
    name = station["name"]
    print(f"Pulling data for station: {name}")
    STATION = station["id"]
    time.sleep(delay)

    all_rows = []
    ## years cycle
    for x in range(start_year, end_year+1):
        time.sleep(delay)
        print(f"year: {x}")
        start_date1 = dt(x, 1, 1)
        end_date1 = dt(x, 7, 31)
        start_date2 = dt(x, 8, 1)
        end_date2 = dt(x, 12, 31)

        start1 = start_date1.strftime("%Y-%m-%d")
        end1 = end_date1.strftime("%Y-%m-%d")
        # first half
        offset = 1
        while True:
            print("front half")
            params = {
                "datasetid": "GHCND",
                "stationid": STATION,
                "startdate": start1,
                "enddate": end1,
                "limit": 1000,
                "offset": offset,
                "datatypeid": ["TAVE", "PRCP", "SNOW", "SNWD", "TMAX", "TMIN", "TOBS", "WT01", "WT03", "WT06", "WT11", "DAPR", "MDPR"]

            }

            r = requests.get(url, headers=headers, params=params)
            print("STATUS:", r.status_code)
            rcount = 0
            while not (r.status_code == 200) and rcount < 20:
                # retry
                rcount += 1
                print("retrying ...")
                time.sleep(5 + rcount)
                r = requests.get(url, headers=headers, params=params)
                print("STATUS:", r.status_code)
            data = r.json()

            if "results" not in data:
                break

            all_rows.extend(data["results"])
            offset += 1000
            time.sleep(delay)

        start2 = start_date2.strftime("%Y-%m-%d")
        end2 = end_date2.strftime("%Y-%m-%d")
        # 2nd half
        offset = 1
        while True:
            print("back half")
            time.sleep(delay)
            params = {
                "datasetid": "GHCND",
                "stationid": STATION,
                "startdate": start2,
                "enddate": end2,
                "limit": 1000,
                "offset": offset,
                "datatypeid": ["TAVE", "PRCP", "SNOW", "SNWD", "TMAX", "TMIN", "TOBS", "WT01", "WT03", "WT06", "WT11", "DAPR", "MDPR"]
            }

            r = requests.get(url, headers=headers, params=params)
            print("STATUS:", r.status_code)
            rcount = 0
            while not (r.status_code == 200) and rcount < 20:
                # retry
                rcount += 1
                print("retrying ...")
                time.sleep(5 + rcount)
                r = requests.get(url, headers=headers, params=params)
                print("STATUS:", r.status_code)
            data2 = r.json()
            if "results" not in data2:
                break
            all_rows.extend(data2["results"])
            offset += 1000

    title = station["id"] + "_" + str(start_year) + "_" + str(end_year)
    temp = title.split(":")
    title = temp[1]
    df = pd.DataFrame(all_rows)
    print(df.head())
    df.to_csv(title+".csv")
    # second half
    

"""
print(start_date.isoformat())
breakpoint()

buffer = BytesIO()
url = f"https://api.weather.gov/stations/{station}/observations"

c = pycurl.Curl()
c.setopt(c.URL, url)
"""