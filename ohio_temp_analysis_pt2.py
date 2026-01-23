import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import math
import itertools
import os
import numpy as np
import bisect

# date/value lookup function, binary search tree
def value_for_date(data, dates, target_date):
    i = bisect.bisect_left(dates, target_date)
    return data[i][1] if i < len(data) and dates[i] == target_date else None

folder = "./data/ohio_weather_data_rev2"
date_format = "%Y-%m-%d"

# Covariance matrix of different observation stations

# Generate date range corresponding to period of interest
oneday = dt.timedelta(days=1)
date_list = [dt.datetime(1990, 1, 1)] 
while date_list[-1] != dt.datetime(2025, 12, 1):
    date_list.append(date_list[-1]+oneday)

stations = [x[1] for x in pd.read_csv("./helper scripts/stations_list_rev3.csv").iterrows()] #load stations into
station_id = [x["id"].split(':')[1] for x in stations]
stations_reorder = []

# loads all datasets, averages temp in accordance with standard practices (min-max)/2
filedata = []
ave_list = []
var_list = []
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
        ave = sum(day_ave)/len(day_ave)
        ave_list.append(ave)
        var = sum([x**2 for x in day_ave])/len(day_ave) - ave**2
        var_list.append(var)
    except:
        breakpoint()

    filedata.append(tlist)

## numbered stations list corresponding to the order of filedata
stations_n = [(i,x) for i, x in enumerate(stations_reorder)]


## basic experiment
## Question: Is there a relationship between station-station distance and station obeservation covariance?
## Hypothesis: Given the nature of environmental conditions being tied to geographic features, I predict an inverse relationship between 
## station-station distance and covariance. 

## Compute all covariance pairs and euclidean distances
dist_list = []
cov_list = []
corr_list = []
for i, cov_pair in enumerate(itertools.combinations(stations_n, 2)):
    print(f"run number: {i} ################################")
    data1 = cov_pair[0]
    data2 = cov_pair[1]

    # retrieve average, variance, and dataset for pair
    dataset1 = filedata[data1[0]]
    dataset2 = filedata[data2[0]]
    
    ave1 = ave_list[data1[0]]
    ave2 = ave_list[data2[0]]

    var1 = var_list[data1[0]]
    var2 = var_list[data2[0]]

    vals1 = [x[1] for x in dataset1]
    vals2 = [x[1] for x in dataset2]
    
    ## calculate Euclidean distance, correcting for curvature and converting to miles, roughly
    lat_d = 69.0*abs(data1[1].lat - data2[1].lat)
    scaler = math.cos((data1[1].lat + data2[1].lat)/2*math.pi/180)
    lon_d = 69.172*scaler*abs(data1[1].lon - data2[1].lon)
    dist_list.append(math.sqrt(lat_d**2 + lon_d**2))

    # align dates
    cov = 0 
    sum_cov = 0
    nn = 0
    dates1 = [d for d,_ in dataset1]
    dates2 = [d for d,_ in dataset2]
    for date in date_list:
        val1 = value_for_date(dataset1, dates1, date)
        val2 = value_for_date(dataset2, dates2, date)
        if not (val2 == None or val1 == None):
            sum_cov += (val1 - ave1)*(val2 - ave2)
            nn += 1
    try:
        cov = sum_cov/nn
        cov_list.append(cov)
    except:
        cov_list.append(0) # should really be NA
    
    ## calculate correlation coefficient
    corr_list.append(cov/(math.sqrt(var1)*math.sqrt(var2)))


# create nxn covariance matrix
station_pairs = list(itertools.combinations(stations_n, 2))

column_row_header = []
row_data = []
# build covariance matrix
for station1 in stations_n:
    print(station1[1].id)
    column_row_header.append(station1[1].id)
    row = dict()
    for station2 in stations_n:
        print(station1[1]["name"], "###", station2[1]["name"])
        if station1 == station2:
            row[station1[1].id] = var_list[station1[0]]
        else:
            cov_ind = next(i for i, pair in enumerate(station_pairs) if pair[0][1]["name"] == station1[1]["name"] and pair[1][1]["name"] == station2[1]["name"]
            or pair[0][1]["name"] == station2[1]["name"] and pair[1][1]["name"] == station1[1]["name"])
            row[station2[1].id] = cov_list[station1[0]]
    row_data.append(row)
cov_matrix = pd.DataFrame(row_data)

fig, ax = plt.subplots(figsize=(8, 6))

im = ax.imshow(cov_matrix.values, cmap='coolwarm')

# Colorbar
plt.colorbar(im, ax=ax)

# Tick labels
ax.set_xticks(np.arange(len(cov_matrix.columns)))
ax.set_yticks(np.arange(len(cov_matrix.index)))
ax.set_xticklabels(cov_matrix.columns)
ax.set_yticklabels(cov_matrix.index)

# Rotate x-axis labels
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

ax.set_title("Covariance Matrix Heatmap")

plt.tight_layout()
plt.show()

breakpoint()