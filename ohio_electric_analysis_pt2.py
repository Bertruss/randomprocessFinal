import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os
from collections import defaultdict
import pickle
import math

with open("e_data_prepped.pkl", "rb") as f:
    data = pickle.load(f)

fueltypelist = ["AOR", "COW", "FOS", "HYC", "NG", "PET", "SUN", "WND", "NUC"]
sectorList = ["All Sectors", "Residential", "All Commercial", "All Industrial", "Electric Utility"]
sectorListID = [99, 8, 96, 97, 1]
fuelType = data["fuelType"]
fuelDesc = data["fuelDesc"]
sectorID = data["sectorID"]
sectorDesc = data["sectorDesc"]
fuel_data = data["data"]

"""
period - YYYY-MM
costPerBtu - dollars per million Btu
generation - thousand megawatthours
totalConsumption
totalConsumptionUnits
"""
format = "%Y-%m"

# Generate date range indpendent of set coverage for single year
onemonth = dt.timedelta(months=1)
date_list = [dt.datetime(1990, 1, 1)] 
while date_list[-1] != dt.datetime(2025, 12, 1):
    date_list.append(date_list[-1]+onemonth)

e_data_basic_analysis = []
# characterize the monthly statistics for different fuel types
for fuel in fueltypelist:
    temp = fuel_data[fuel][99]
    dates = [pd.to_datetime(s, format="%Y-%m") for s in temp["period"]]
    vals = temp["generation"]

    mean_vals = []
    var_vals = []
    dev_vals = []
    date_vals = []
    if any(math.isnan(x) for x in vals):
        breakpoint()
    for month in date_list:
        vals_sub = [val for date, val in zip(dates, vals) if date.month == month.month]
        month_mean = sum(vals_sub)/len(vals_sub)
        month_variance = sum([(x - month_mean)**2 for x in vals_sub])/(len(vals_sub) - 1)

        mean_vals.append(month_mean)
        var_vals.append(month_variance)
        dev_vals.append(math.sqrt(month_variance))
        date_vals.append(month)
    fuel_data_analysis = {
        "mean" : mean_vals,
        "var" : var_vals,
        "dev" : dev_vals,
        "date" : date_vals
    }
    e_data_basic_analysis.append(fuel_data_analysis)


with open("e_data_basic.pkl", "wb") as f:
    pickle.dump(e_data_basic_analysis, f, protocol=pickle.HIGHEST_PROTOCOL)
breakpoint()



