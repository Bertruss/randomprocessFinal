import pickle
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
with open("monthly_temp_results_pt1.pkl", "rb") as f:
    ohio_monthly_temp = pickle.load(f)

with open("e_data_prepped.pkl", "rb") as f:
    data = pickle.load(f)

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
temp  = [b for a, b in zip(month_date, monthly_ave) if a in dates]
breakpoint()
## solving for linear prediction/correlation
temp_mean = sum(temp)/len(temp)
sales_mean = sum(res_sales)/len(res_sales)

temp_var = sum([(x - temp_mean)**2 for x in temp])/len(temp)
sales_var = sum([(x - sales_mean)**2 for x in res_sales])/len(res_sales)

ts_cov = sum ((temp-temp_mean)*(sale-sales_mean) for sale, temp in zip(res_sales, temp))/len(temp)

Corr_coef = ts_cov/(math.sqrt(temp_var)*math.sqrt(sales_var))

linear_pred = (lambda x: sales_mean - (ts_cov/temp_var)*temp_mean + (ts_cov/temp_var)*x)

pred_line = [linear_pred(t) for t in temp]
linear_mse = sum([(act-pred)**2 for act, pred in zip(res_sales, pred_line)])/len(pred_line)
breakpoint()
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
t2s_cov = sum ((temp-temp_mean)**2*(sales-sales_mean) for sales, temp in zip(res_sales, temp))/len(temp)

denom = temp_var*(u4_temp - temp_var**2) - u3_temp**2

quad_pred = (lambda x: sales_mean
 + (ts_cov*(u4_temp-temp_var**2)-t2s_cov*u3_temp)/denom*(x - temp_mean)
 + (t2s_cov*temp_var - ts_cov*u3_temp)/denom*((x - temp_mean)**2 - temp_var)) 

pred_quad = [quad_pred(x) for x in temp]q
quad_mse = sum([(act-pred)**2 for act, pred in zip(res_sales, pred_quad)])/len(pred_quad)

temp_range = np.linspace(min(temp), max(temp), 100)
pred_quad = [quad_pred(x) for x in temp_range]
pred_line = [linear_pred(t) for t in temp_range]

fig, ax = plt.subplots()
plt.plot(temp, res_sales, '.', label="temp-sales pairs")
plt.plot(temp_range, pred_quad, label="Quadratric prediction")
plt.plot(temp_range, pred_line, label="Linear prediction")
plt.title("Temperature vs Energy costs")
plt.xlabel("Temperature (F)")
plt.ylabel("Price (¢/KWhr)")
plt.legend()
ax.text(temp_range[50], pred_quad[50], f"MSE = {quad_mse:.5g}", color="black", fontsize=12, ha="left", va="bottom")
ax.text(temp_range[50], pred_line[50], f"MSE = {linear_mse:.5g}", color="black", fontsize=12, ha="left", va="bottom")
fig.canvas.manager.set_window_title("Linear vs Quad fit: Temperature vs Residential Sales")
plt.show(block=False)
breakpoint()



### what if we try instead predicting against temperature's distance from the mean:
temp = [math.abs(x-temp_mean) for x in temp]

# re-using code
temp_mean = sum(temp)/len(temp)
temp_var = sum([(x - temp_mean)**2 for x in temp])/len(temp)
ts_cov = sum ((temp-temp_mean)*(sales-sales_mean) for sale, temp in zip(res_sales, temp))/len(temp)
Corr_coef = ts_cov/(math.sqrt(temp_var)*math.sqrt(sales_var))
linear_pred = (lambda x: sales_mean - (ts_cov/temp_var)*temp_mean + (ts_cov/temp_var)*x)
pred_line = [linear_pred(t) for t in temp]
linear_mse = sum([(act-pred)**2 for act, pred in zip(res_sales, pred_line)])/len(pred_line)
breakpoint()


u3_temp = sum([(x-temp_mean)**3 for x in temp])/len(temp)
u4_temp = sum([(x-temp_mean)**4 for x in temp])/len(temp)
t2s_cov = sum ((temp-temp_mean)**2*(sales-sales_mean) for sales, temp in zip(res_sales, temp))/len(temp)

denom = temp_var*(u4_temp - temp_var**2)-u3_temp**2
quad_pred = (lambda x: sales_var + (ts_cov*(u4_temp-temp_var**2)-t2s_cov*u3_temp)/d*(x-temp_mean) + (t2s_cov*temp_var - ts_cov*u3_temp)/d*((x - temp_mean)**2 - temp_var)) 
pred_quad = [quad_pred(x) for x in temp]
quad_mse = sum([(act-pred)**2 for act, pred in zip(res_sales, pred_quad)])/len(pred_quad)



breakpoint()