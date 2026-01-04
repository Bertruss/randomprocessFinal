import json
from datetime import datetime as dt
import pandas as pd

start_date = dt(1990, 1, 1)
end_date = dt(2025, 1, 1)

data = pd.read_csv("ohio_stations_list.csv")

listy = pd.DataFrame()

listz = pd.DataFrame()

for entry in data.iterrows():
    entry = entry[1]
    min_date = dt.strptime(entry["mindate"], "%Y-%m-%d")
    max_date = dt.strptime(entry["maxdate"], "%Y-%m-%d")
    
    name = entry["name"]
    id = entry["id"]
    lat = entry["latitude"]
    lon = entry["longitude"]
    coverage = entry["datacoverage"]
    temp = [{"name":name, "id":id, "cov":coverage, "lat":lat, "lon":lon }]
    new_thing = pd.DataFrame(temp)
    if(start_date >= min_date and max_date >=end_date and coverage == 1):
        print(id, name)
        print(lat, lon)
        print(min_date, max_date)
        print(coverage)
        listy = pd.concat([listy, new_thing], ignore_index=True)
breakpoint()

for entry in listy.iterrows():
    entry = entry[1]
    name = entry["name"]
    id = entry["id"]
    lat = entry["lat"]
    lon = entry["lon"]
    coverage = entry["cov"]
    temp = pd.DataFrame(entry)
    print(id, name)
    print(lat, lon)
    print(min_date, max_date)
    print(coverage)
    t = input("keep?")
    if t == "y":
        listz = pd.concat([listz, temp], ignore_index=True)
breakpoint()
