import pickle
import pandas as pd
import math

with open("results_pt1.pkl", "rb") as f:
    results_pt1 = pickle.load(f)

with open("e_data_prepped.pkl", "rb") as f:
    data = pickle.load(f)

ohio_monthly_temp = results_pt1["ohio_monthly_temp"]
month_date = ohio_monthly_temp["date"]
monthly_ave = ohio_monthly_temp["tave"]
monthly_var = ohio_monthly_temp["var"]
monthly_dev = ohio_monthly_temp["stddev"]


res_sales = data["res_sales"]
res_period = res_sales["period"]
res_price = res_sales["price"]
res_sales = res_sales["sales"]

## Experiment 2
dates = res_period # the more limited set, 

# limiting temp set 
temp, temp_var, temp_dev  = [b, c, d for a, b, c, d in zip(month_date, monthly_ave, monthly_var, monthly_dev) if a in dates]

# solving for linear prediction/correlation
temp_mean = sum(temp)/len(temp)
sales_mean = sum(res_sales)/len(res_sales)

temp_var = sum([(x - temp_mean)**2 for x in temp])/len(temp)
sales_var = sum([(x - sales_mean)**2 for x in sales_mean])/len(res_sales)

ts_cov = sum ((temp-temp_mean)*(sale-sales_mean) for sales, temp in zip(sales, temp))/len(temp)

Corr_coef = ts_cov/(math.sqrt(temp_var)*math.sqrt(sales_var))

breakpoint()