import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import math
import itertools
import os
import numpy as np
import bisect

import pickle

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

# load stations metadata
stations = [x[1] for x in pd.read_csv("./helper scripts/stations_list_rev3.csv").iterrows()]
station_id = [x["id"].split(':')[1] for x in stations]
stations_reorder = []

# loads all datasets, averages temp in accordance with standard practices (min+max)/2
filedata = []
ave_list = []
var_list = []
for file in os.listdir(folder):
    sid = next(i for i, x in enumerate(station_id) if x == file.split('_')[0])
    print(stations[sid]["name"])
    stations_reorder.append(stations[sid].copy())
    sample = pd.read_csv(folder+'/'+file)
    tmax = sample[sample["datatype"] == "TMAX"] 
    tmin = sample[sample["datatype"] == "TMIN"] 

    dateobj_min = [dt.datetime.fromisoformat(x) for x in tmin["date"]]
    dateobj_max = [dt.datetime.fromisoformat(x) for x in tmax["date"]]
    vals_min = [(x,y) for x,y in zip(tmin["date"].tolist(), tmin["value"].tolist())]
    vals_max = [(x,y) for x,y in zip(tmax["date"].tolist(), tmax["value"].tolist())]
    
    ## Apparently you can not rely on files having both tmax AND tmin for any given date
    # assemble list of synced max/min pairs UGH >:C
    dateobj = [dt.datetime.fromisoformat(x) for x in sample["date"].unique()]
    date_list = []
    vals_list = []
    N = 0
    for date in dateobj:
        tmax_tmp = value_for_date(vals_max, dateobj_max, date)
        tmin_tmp = value_for_date(vals_min, dateobj_min, date)
        if tmin_tmp != None and tmax_tmp != None:
            date_list.append(date)
            vals_list.append((tmax_tmp,tmin_tmp))
        else:
            if (tmin_tmp == None) ^ (tmax_tmp == None):
               N+=1

    day_ave = [(ma+mi)/2 for ma, mi in vals_list]
    tlist = [(date, temp) for date, temp in zip(date_list, day_ave)]
    set_ave = sum(day_ave)/len(day_ave)
    var = sum([(x - set_ave)**2 for x in day_ave])/(len(day_ave) - 1)
    var_list.append(var)
    filedata.append(tlist)

## numbered stations list corresponding to the order of filedata
stations_n = [(i,x) for i, x in enumerate(stations_reorder)]

## Compute all covariance pairs and euclidean distances
dist_list = []
cov_list = []
corr_list = []
station_pairs = []
for i, cov_pair in enumerate(itertools.combinations(stations_n, 2)):
    station_pairs.append(cov_pair)
    print(f"run number: {i} ################################")
    data1 = cov_pair[0]
    data2 = cov_pair[1]

    # retrieve average, variance, and dataset for pair
    dataset1 = filedata[data1[0]]
    dataset2 = filedata[data2[0]]
    
    vals1 = [x[1] for x in dataset1]
    vals2 = [x[1] for x in dataset2]
    
    ## calculate Euclidean distance, correcting for curvature and converting to miles, roughly
    lat_d = 69.0*abs(data1[1].lat - data2[1].lat)
    scaler = math.cos((data1[1].lat + data2[1].lat)/2*math.pi/180)
    lon_d = 69.172*scaler*abs(data1[1].lon - data2[1].lon)
    dist_list.append(math.sqrt(lat_d**2 + lon_d**2))

    # Must compute the variance and ave of the overlapping set
    # Create subsets consisting of date aligned data
    dates1 = [d for d,_ in dataset1]
    dates2 = [d for d,_ in dataset2]
    sub1_list = []
    sub2_list = []
    cov_pairs = []
    for date in date_list:
        val1 = value_for_date(dataset1, dates1, date)
        val2 = value_for_date(dataset2, dates2, date)
        if not (val2 == None or val1 == None):
            sub1_list.append(val1)
            sub2_list.append(val2)
            cov_pairs.append((val1, val2))
    
    if len(sub1_list) <= 1:
        # The case where two datasets have little or no overlap
        corr = math.nan
        cov = math.nan
    else:
        # mean
        ave1 = sum(sub1_list)/len(sub1_list)
        ave2 = sum(sub2_list)/len(sub2_list)
        
        # variance
        var1 = sum([(x - ave1)**2 for x in sub1_list])/(len(sub1_list)-1)    
        var2 = sum([(x - ave2)**2 for x in sub2_list])/(len(sub2_list)-1) 

        # covariance
        cov = sum([(x - ave1)*(y - ave2) for x,y in cov_pairs])/(len(cov_pairs)-1)       
        
        # correlation
        corr = cov/(math.sqrt(var1)*math.sqrt(var2))
    cov_list.append(cov)    
    corr_list.append(corr)

column_row_header = []
row_data = []
# build covariance matrix
for station1 in stations_n:
    print(station1[1].id)
    column_row_header.append(station1[1]["name"].split(',')[0])
    row = dict()
    for station2 in stations_n:
        print(station1[1]["name"], "###", station2[1]["name"])
        namestring = station2[1]["name"].split(',')[0] + " | " + station2[1]["id"]
        if station1 == station2:
            row[namestring] = var_list[station1[0]]
        else:
            cov_ind = next(i for i, pair in enumerate(station_pairs) if pair[0][1]["name"] == station1[1]["name"] and pair[1][1]["name"] == station2[1]["name"]
            or pair[0][1]["name"] == station2[1]["name"] and pair[1][1]["name"] == station1[1]["name"])
            row[namestring] = cov_list[cov_ind]
    row_data.append(row)
cov_matrix = pd.DataFrame(row_data)

## Calculate correlation coefficient between correlation coefficient and euclidean distance
ave_dist = sum(dist_list)/len(dist_list)
ave_corr = sum(corr_list)/len(corr_list)

var_corr = sum([(d - ave_corr)**2 for d in corr_list])/(len(corr_list) - 1)
var_dist = sum([(d - ave_dist)**2 for d in dist_list])/(len(dist_list) - 1)
dist_corr_covariance = sum([(d-ave_dist)*(c-ave_corr)for d, c, in zip(dist_list, corr_list)])/(len(dist_list) - 1)
coef = dist_corr_covariance/(math.sqrt(var_dist)*math.sqrt(var_corr))

results_pt2 = {
    "coef" : coef,
    "dist_list": dist_list,
    "corr_list": corr_list,
    "cov_matrix": cov_matrix,
    "ave_list": ave_list,
    "var_list": var_list,
    "filedata": filedata
}

with open("results_pt2.pkl", "wb") as f:
    pickle.dump(results_pt2, f, protocol=pickle.HIGHEST_PROTOCOL)

breakpoint()