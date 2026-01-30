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
breakpoint()
# limiting temp set 
temp  = [b for a, b in zip(month_date, monthly_ave) if a in dates]

## solving for linear prediction/correlation
temp_mean = sum(temp)/len(temp)
sales_mean = sum(res_sales)/len(res_sales)

temp_var = sum([(x - temp_mean)**2 for x in temp])/len(temp)
sales_var = sum([(x - sales_mean)**2 for x in sales_mean])/len(res_sales)

ts_cov = sum ((temp-temp_mean)*(sale-sales_mean) for sales, temp in zip(sales, temp))/len(temp)

Corr_coef = ts_cov/(math.sqrt(temp_var)*math.sqrt(sales_var))

linear_pred = (lambda x: sales_mean - (ts_cov/temp_var)*temp_mean + (ts_cov/temp_var)*x)

pred_line = [linear_pred(t) for t in temp]
linear_mse = sum([(act-pred)**2 for act, pred in zip(res_sales, pred_line)])/len(pred_line)

## solving for qaudratic prediction

"""
E(x)
E(y)
var(x)
cov(x, y)

New moments
u3 = E[(X-ux)^3]
u4 = E[(X-ux)^4]
cov(x2, y) = E[(X-ux)^2*(Y-uy)]
"""
u3_temp = sum([(x-temp_mean)**3 for x in temp])/len(temp)
u4_temp = sum([(x-temp_mean)**4 for x in temp])/len(temp)
t2s_cov = sum ((temp-temp_mean)**2*(sale-sales_mean) for sales, temp in zip(sales, temp))/len(temp)

denom = temp_var*(u4_temp - temp_var**2)-u3_temp**2

sales_var + (ts_cov*(u4_temp-temp_var**2)-t2s_cov*u3_temp)/d*(x-temp_mean) + (t2s_cov*temp_var - )

breakpoint()