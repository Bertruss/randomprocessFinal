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
com = data["com_sales"]
res = data["res_sales"]
"""
period - YYYY-MM
costPerBtu - dollars per million Btu
generation - thousand megawatthours
totalConsumption
totalConsumptionUnits
"""
format = "%Y-%m"

# Generate date range indpendent of set coverage for single year
date_list = pd.period_range("1990-01", "1990-12", freq="M")
date_list = [pd.to_datetime(date, format="%Y-%m") for date in date_list]

basic_analysis = []
# characterize the monthly statistics for different fuel types
for fuel in fueltypelist:
    print(fuel)
    temp = fuel_data[fuel][99]
    dates = [pd.to_datetime(s, format="%Y-%m") for s in temp["period"]]
    vals = temp["generation"]

    mean_vals = []
    var_vals = []
    dev_vals = []
    date_vals = []
    skew_vals = []
    if any(math.isnan(x) for x in vals):
        # it's necessary to handle nans here as they would mess up further calculations
        cleaned = [(month, val) for month, val in zip(dates, vals) if not math.isnan(val)] 
        dates = [x for x, _ in cleaned]
        vals = [x for _, x in cleaned]
    for month in date_list:
        vals_sub = [val for date, val in zip(dates, vals) if date.month == month.month]
        month_mean = sum(vals_sub)/len(vals_sub)
        month_variance = sum([(x - month_mean)**2 for x in vals_sub])/(len(vals_sub) - 1)
        month_dev = math.sqrt(month_variance)
        month_skew = sum([((x-month_mean)**3)for x in vals_sub])/((len(vals_sub)-1)*month_dev**3)
        mean_vals.append(month_mean)
        var_vals.append(month_variance)
        dev_vals.append(month_dev)
        skew_vals.append(month_skew)
        date_vals.append(month)
    fuel_data_analysis = {
        "mean" : mean_vals,
        "var" : var_vals,
        "dev" : dev_vals,
        "skew" : skew_vals,
        "date" : date_vals
    }
    basic_analysis.append(fuel_data_analysis)

res_sales = data["res_sales"]
com_sales = data["com_sales"]

com_period = com_sales["period"]
com_price = com_sales["price"]
com_sales = com_sales["sales"]

res_period = res_sales["period"]
res_price = res_sales["price"]
res_sales = res_sales["sales"]

com_price_mean_list = []
com_price_var_list = []
com_sales_mean_list = []
com_sales_var_list = []

res_price_mean_list = []
res_price_var_list = []
res_sales_mean_list = []
res_sales_var_list = []


for month in date_list:
    print(month.month)
    com_price_tmp = [x for x, date in zip(com_price, com_period) if date.month == month.month]
    com_sales_tmp = [x for x, date in zip(com_sales, com_period) if date.month == month.month]
    res_price_tmp = [x for x, date in zip(res_price, res_period) if date.month == month.month]
    res_sales_tmp = [x for x, date in zip(res_sales, res_period) if date.month == month.month]
    
    com_price_mean = sum(com_price_tmp)/len(com_price_tmp)
    com_price_var = sum([(x - com_price_mean)**2 for x in com_price_tmp])/(len(com_price_tmp) - 1)
    com_sales_mean = sum(com_sales_tmp)/len(com_sales_tmp)
    com_sales_var = sum([(x - com_sales_mean)**2 for x in com_sales_tmp])/(len(com_sales_tmp) - 1)
    res_price_mean = sum(res_price_tmp)/len(res_price_tmp)
    res_price_var = sum([(x - res_price_mean)**2 for x in res_price_tmp])/(len(res_price_tmp) - 1)
    res_sales_mean = sum(res_sales_tmp)/len(res_sales_tmp)
    res_sales_var = sum([(x - res_sales_mean)**2 for x in res_sales_tmp])/(len(res_sales_tmp) - 1)

    com_price_mean_list.append(com_price_mean)
    com_price_var_list.append(com_price_var)
    com_price_std_list = [math.sqrt(x) for x in com_price_var_list]

    com_sales_mean_list.append(com_sales_mean)
    com_sales_var_list.append(com_sales_var)
    com_sales_std_list = [math.sqrt(x) for x in com_sales_var_list]
    
    res_price_mean_list.append(res_price_mean)
    res_price_var_list.append(res_price_var)
    res_price_std_list = [math.sqrt(x) for x in res_price_var_list]
    
    res_sales_mean_list.append(res_sales_mean)
    res_sales_var_list.append(res_sales_var)
    res_sales_std_list = [math.sqrt(x) for x in res_sales_var_list]

com_moments = {
    "com_price_mean" : com_price_mean_list,
    "com_price_var" : com_price_var_list,
    "com_price_std" : com_price_std_list,
    "com_sales_mean" : com_sales_mean_list,
    "com_sales_var" : com_sales_var_list,
    "com_sales_std" : com_sales_std_list
}

res_moments = {
    "res_price_mean_list" : res_price_mean_list,
    "res_price_var_list" : res_price_var_list,
    "res_price_std_list" : res_price_std_list,
    "res_sales_mean_list" : res_sales_mean_list,
    "res_sales_var_list" : res_sales_var_list,
    "res_sales_std_list" : res_sales_std_list
}

complete_basic_analysis = {
    "date_list" : date_list,
    "basic_analysis" : basic_analysis,
    "com_moments" : com_moments,
    "res_moments" : res_moments
}


## Experiment 2



with open   ("e_data_basic.pkl", "wb") as f:
    pickle.dump(complete_basic_analysis, f, protocol=pickle.HIGHEST_PROTOCOL)
breakpoint()



