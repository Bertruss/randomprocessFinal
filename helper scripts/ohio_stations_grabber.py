import requests
import json
import pandas as pd
import pycurl
from io import BytesIO
from datetime import datetime as dt
with open("token.txt", "r") as file:
    token = file.readline()
headers = {"token": token}


# pull all stations in the state of ohio
stations_req = "https://www.ncei.noaa.gov/cdo-web/api/v2/datatypes"
r = requests.get(stations_req, headers=headers)
data = r.json()

filename = "station_data.json"
f = open(filename, 'w')
f.write(json.dumps(data, indent=2))
f.close()
breakpoint()



start_date = dt(1990, 1, 1)
end_date = dt(2025, 1, 1)

url = "https://www.ncei.noaa.gov/cdo-web/api/v2/"


"""
print(start_date.isoformat())
breakpoint()

buffer = BytesIO()
url = f"https://api.weather.gov/stations/{station}/observations"

c = pycurl.Curl()
c.setopt(c.URL, url)
"""