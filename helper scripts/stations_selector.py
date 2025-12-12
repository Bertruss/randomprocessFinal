import json
from datetime import datetime as dt
import pandas as pd

start_date = dt(1990, 1, 1)
end_date = dt(2025, 1, 1)

with open("station_data.json") as f:
    data = json.load(f)

listy = pd.DataFrame()

for entry in data["results"]:
    min_date = dt.strptime(entry["mindate"], "%Y-%m-%d")
    max_date = dt.strptime(entry["maxdate"], "%Y-%m-%d")
    
    name = entry["name"]
    id = entry["id"]
    lat = entry["latitude"]
    lon = entry["longitude"]
    coverage = entry["datacoverage"]
    temp = [{"name":name, "id":id, "lat":lat, "lon":lon }]
    new_thing = pd.DataFrame(temp)
    if(start_date >= min_date and max_date >=end_date):
        print(id, name)
        print(lat, lon)
        print(min_date, max_date)
        t = input("keep?")
        if t == "y":
            listy = pd.concat([listy, new_thing], ignore_index=True)
breakpoint()
