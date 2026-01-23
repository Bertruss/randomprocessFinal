import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import math
import itertools
import os

folder = "./data/ohio_weather_data_rev2"
date_format = "%Y-%m-%d"

# Covariance matrix of different observation stations

# Generate date range indpendent of set coverage
oneday = dt.timedelta(days=1)
date_list = [dt.datetime(1990, 1, 1)] 
while date_list[-1] != dt.datetime(2025, 12, 1):
    date_list.append(date_list[-1]+oneday)

stations = [x[1] for x in pd.read_csv("./helper scripts/stations_list_rev3.csv").iterrows()] #load stations into
station_id = [x["id"].split(':')[1] for x in stations]
stations_reorder = []

# flatten all datasets, averages temp in accordance with standard practices (min-max)/2
filedata = []
ave_list = []
for file in os.listdir(folder):
    sid = next(i for i, x in enumerate(station_id) if x == file.split('_')[0])
    stations_reorder.append(stations[sid].copy())
    sample = pd.read_csv(folder+'/'+file)
    tmax = sample[sample["datatype"] == "TMAX"] 
    tmin = sample[sample["datatype"] == "TMIN"] 
        
    dateobj = [dt.datetime.fromisoformat(x) for x in tmin["date"]]
    day_ave = [(ma-mi)/2 for mi, ma in zip(tmin["value"], tmax["value"])]
    tlist = [(date, temp) for date, temp in zip(dateobj, day_ave)]
    try:
        ave_list.append(sum(day_ave)/len(day_ave))
    except:
        breakpoint()

    filedata.append(tlist)

## numbered stations list corresponding to the order of filedata
stations_n = [(i,x) for i, x in enumerate(stations_reorder)]


## all covariance pairs
## small experiment
## Question: Is there a relationship between observation station distance and station obeservation covariance?
## Hypothesis: Given the nature of environmental conditions being tied to geographic features, I predict a high degree of correlation. 

dist_list = []
cov_list = []
for i, cov_pair in enumerate(itertools.combinations(stations_n, 2)):
    print(f"run number: {i} ################################")
    data1 = cov_pair[0]
    data2 = cov_pair[1]

    dataset1 = filedata[data1[0]]
    dataset2 = filedata[data2[0]]
    
    ave1 = ave_list[data1[0]]
    ave2 = ave_list[data2[0]]

    vals1 = [x[1] for x in dataset1]
    vals2 = [x[1] for x in dataset2]
    
    
    lat_d = abs(data1[1].lat - data2[1].lat)
    lon_d = abs(data1[1].lon - data2[1].lon)
    
    dist_list.append(math.sqrt(lat_d**2 + lon_d**2))

    # align dates
    sum_cov = 0
    n = 0
    for date in date_list:
        val1 = next((date_val[1] for date_val in dataset1 if date_val[0] == date), None)
        val2 = next((date_val[1] for date_val in dataset2 if date_val[0] == date), None)
        if val2 == None or val1 == None:
            b = 0
            #if val2 == None:
            #  print(f"{date.day}-{date.month}-{date.year} val1:{val1}, val2:{val2} #######")
            #if val1 == None:
            #   print(f"{date.day}-{date.month}-{date.year} val1:{val1}, val2:{val2} #######")
        else:
            sum_cov += (val1 - ave1)*(val2 - ave2)
            n += 1
            #print(f"{date.day}-{date.month}-{date.year} val1:{val1}, val2:{val2}")
    cov_list.append(sum_cov/n)

breakpoint()
# create nxn covariance matrix