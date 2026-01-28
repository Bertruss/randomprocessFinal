import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import math
import itertools
import os
import numpy as np
import bisect
import matplotlib.dates as mdates
import pickle

with open("results_pt1.pkl", "rb") as f:
    results_pt1 = pickle.load(f)

with open("results_pt2.pkl", "rb") as f:
    results_pt2 = pickle.load(f)

ohio_typical_year_temp = results_pt1["ohio_typical_year_temp"]
ohio_monthly_temp = results_pt1["ohio_monthly_temp"]
ohio_average_temp = results_pt1["ohio_average_temp"]

"""
results_pt2 = {
    "coef": coef,
    "dist_list": dist_list,
    "corr_list": corr_list,
    "cov_matrix": cov_matrix,
    "ave_list": ave_list,
    "var_list": var_list,
    "filedata": filedata
}
"""

year_date_list = ohio_typical_year_temp["date"]
ave = ohio_typical_year_temp["tave"]
var = ohio_typical_year_temp["var"]
dev = ohio_typical_year_temp["stddev"]
skew = ohio_typical_year_temp["skew"]

month_date = ohio_monthly_temp["date"]
monthly_ave = ohio_monthly_temp["tave"]
monthly_var = ohio_monthly_temp["var"]
monthly_dev = ohio_monthly_temp["stddev"]
monthly_skew = ohio_monthly_temp["skew"]

date_list = ohio_average_temp["date"]
day_ave = ohio_average_temp["tave"]
day_var = ohio_average_temp["var"]
day_dev = ohio_average_temp["stddev"]
day_skew = ohio_average_temp["skew"] 

date_aligned_dataset = results_pt1["date_aligned_dataset"]

## lets do some smoothing for the sake of prettiness
def smooth(vals, window):
    if not (window % 2):
        print("odd pad only")
        exit()
    pad_vals = vals[-2*window:] + vals + vals[:2*window] # pad
    vals_smooth = np.convolve(pad_vals, np.ones(window)/window, mode='valid') # smooth
    tmp = int((window-1)/2)  #depad
    return vals_smooth[2*window-tmp:-2*window+tmp]

window = 15
ave_smooth = smooth(ave, window)
dev_smooth = smooth(dev, window)
skew_smooth = smooth(skew, window)

modeish = [a - c*b for a, b, c in zip(ave_smooth, dev_smooth, skew_smooth)]

minave_3 = [mean-3*dev for mean,dev in zip(ave_smooth, dev_smooth)]
maxave_3 = [mean+3*dev for mean,dev in zip(ave_smooth, dev_smooth)]
minave_2 = [mean-2*dev for mean,dev in zip(ave_smooth, dev_smooth)]
maxave_2 = [mean+2*dev for mean,dev in zip(ave_smooth, dev_smooth)]
minave_1 = [mean-1*dev for mean,dev in zip(ave_smooth, dev_smooth)]
maxave_1 = [mean+1*dev for mean,dev in zip(ave_smooth, dev_smooth)]


## Pretty graphs made with the assistance of chatGPT

## plot select
### DATA SUMMARY PLOT
mean_color = "#4C72B0"   # muted blue
mode_color = "#55A868"   # muted green
std_color  = "#DD8452"   # muted orange
scatter_color = "#c8fcbd" #"#d4cda9"


r = input("render temp summary plot?")
if r == 'y':
    plt.plot(
        year_date_list,
        ave_smooth,
        color=mean_color,
        linewidth=2,
        label="Mean"
    )

    plt.plot(
        year_date_list,
        modeish,
        color=mode_color,
        linestyle="--",
        linewidth=2,
        label="Mode (approx. from skewness)"
    )

    # ±3σ shaded regions
    plt.fill_between(
        year_date_list,
        maxave_3,
        minave_3,
        color=std_color,
        alpha=0.25,
        linewidth=0,
        label="±3σ from mean"
    )

    # Inner bands (no labels to avoid legend duplication)
    plt.fill_between(
        year_date_list,
        maxave_2,
        minave_2,
        color=std_color,
        alpha=0.18,
        linewidth=0
    )

    plt.fill_between(
        year_date_list,
        maxave_1,
        minave_1,
        color=std_color,
        alpha=0.12,
        linewidth=0
    )

    plt.title("Typical Ohio Year")
    plt.grid()
    plt.legend(loc="best", framealpha=0.9)
    plt.margins(x=0)

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))

    ax.set_xlabel("Month")
    ax.set_ylabel("Temperature (°F)")
    ax.autoscale(axis="y", tight=True)

    plt.show(block=False)
    fig = plt.gcf()
    fig.canvas.manager.set_window_title("Typical Ohio Year")
"""
### DENSE DATA PLOT
fig2, ax2 = plt.subplots()
plt.plot(
    year_date_list,
    ave_smooth,
    color=mean_color,
    linewidth=2,
    label="Mean"
)

plt.plot(
    year_date_list,
    modeish,
    color=mode_color,
    linestyle="--",
    linewidth=2,
    label="Mode (approx. from skewness)"
)

# draw individual data points
x = np.repeat(year_date_list, [len(v) for v in date_aligned_dataset])
y = np.concatenate(date_aligned_dataset)

plt.scatter(
    x,
    y,
    s=7,
    alpha=0.005,
    color="black"
)

plt.title("Typical Ohio Year")
plt.grid(axis="y")
plt.legend(loc="best", framealpha=0.9)
plt.margins(x=0)

ax2.xaxis.set_major_locator(mdates.MonthLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b"))

ax2.set_xlabel("Day of Year")
ax2.set_ylabel("Temperature (°F)")
ax2.autoscale(axis="y", tight=True)

plt.show(block=False)
fig2.canvas.manager.set_window_title("Typical Ohio Year")
breakpoint()
"""

## show winter centered plot
r = input("render temp summary plot (winter centered)?")
if r == 'y':
    SHIFT_MONTHS = 6
    def shift_dates(dates):
        return pd.to_datetime(dates) + pd.DateOffset(months=SHIFT_MONTHS)

    # ---- shift all x-values ----
    dates_shifted = shift_dates(year_date_list)

    x = np.repeat(year_date_list, [len(v) for v in date_aligned_dataset])
    x_shifted = shift_dates(x)

    shift = 182
    breakpoint()
    ave_smooth = np.concatenate((ave_smooth[shift:], ave_smooth[:shift])) 
    dev_smooth = np.concatenate((dev_smooth[shift:], dev_smooth[:shift])) 
    skew_smooth = np.concatenate((skew_smooth[shift:], skew_smooth[:shift])) 
    modeish = np.concatenate((modeish[shift:], modeish[:shift])) 
    minave_3 = np.concatenate((minave_3[shift:], minave_3[:shift])) 
    maxave_3 = np.concatenate((maxave_3[shift:], maxave_3[:shift])) 
    minave_2 = np.concatenate((minave_2[shift:], minave_2[:shift])) 
    maxave_2 = np.concatenate((maxave_2[shift:], maxave_2[:shift])) 
    minave_1 = np.concatenate((minave_1[shift:], minave_1[:shift])) 
    maxave_1 = np.concatenate((maxave_1[shift:], maxave_1[:shift])) 

    plt.plot(
        dates_shifted,
        ave_smooth,
        color=mean_color,
        linewidth=2,
        label="Mean"
    )

    plt.plot(
        dates_shifted,
        modeish,
        color=mode_color,
        linestyle="--",
        linewidth=2,
        label="Mode (approx. from skewness)"
    )

    plt.fill_between(
        dates_shifted,
        maxave_3,
        minave_3,
        color=std_color,
        alpha=0.25,
        linewidth=0,
        label="±3σ from mean"
    )

    plt.fill_between(
        dates_shifted,
        maxave_2,
        minave_2,
        color=std_color,
        alpha=0.18,
        linewidth=0
    )

    plt.fill_between(
        dates_shifted,
        maxave_1,
        minave_1,
        color=std_color,
        alpha=0.12,
        linewidth=0
    )

    # ---- axes formatting ----
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))

    ax.set_xlabel("Month")
    ax.set_ylabel("Temperature (°F)")
    ax.autoscale(axis="y", tight=True)

    plt.title("Typical Ohio Year (Winter-Centered)")
    plt.legend(loc="best", framealpha=0.9)
    plt.grid(axis="y")
    plt.margins(x=0)

    plt.show(block=False)

    fig = plt.gcf()
    fig.canvas.manager.set_window_title("Typical Ohio Year (Winter-Centered)")

coef = results_pt2["coef"]
dist_list = results_pt2["dist_list"]
corr_list = results_pt2["corr_list"]
cov_matrix = results_pt2["cov_matrix"]
ave_list = results_pt2["ave_list"]
var_list = results_pt2["var_list"]
filedata = results_pt2["filedata"]

r = input("Render covariance matrix?")
if r == 'y':
    # plot covariance matrix
    fig, ax = plt.subplots(figsize=(8, 6))

    # make NaN mask and set color values
    cov_masked = np.ma.masked_invalid(cov_matrix.values)
    cmap = plt.cm.coolwarm.copy()
    cmap.set_bad(color='black')
    im = ax.imshow(cov_masked, cmap=cmap)
    
    # Colorbar
    plt.colorbar(im, ax=ax)

    # Tick labels
    ax.set_xticks(np.arange(len(cov_matrix.index)))
    ax.set_yticks(np.arange(len(cov_matrix.index)))
    #ax.set_xticklabels(cov_matrix.index)
    ax.set_yticklabels(cov_matrix.columns)

    #Rotate x-axis labels
    #plt.setp(ax.get_xticklabels(), ha='right')

    ax.set_title("Covariance Matrix Heatmap")
    plt.show(block=False)
    fig = plt.gcf()
    fig.canvas.manager.set_window_title("Station Covariance Matrix")


# Notable outliers, lunken, kenton
# lunken = filedata[1]
# kenton = filedata[11]

r = input("Render station spatial coupling plot?")
if r == 'y':
    # draw linear prediction line
    fig, ax = plt.subplots()

    ## exclude nan's
    tmp_corr = []
    tmp_dist = []
    for i,x in enumerate(corr_list):
        if not math.isnan(x):
            tmp_corr.append(x)
            tmp_dist.append(dist_list[i])
    
    corr_list = tmp_corr
    dist_list = tmp_dist

    corr_mean = sum(corr_list)/len(corr_list) # Y
    dist_mean = sum(dist_list)/len(dist_list) # X

    corr_var = sum([(x**2) for x in corr_list])/len(dist_list) - corr_mean**2 # Y
    dist_var = sum([(x**2) for x in dist_list])/len(dist_list) - dist_mean**2 # X

    cd_cov = sum([(x - dist_mean) * (y - corr_mean) for x, y in  zip(dist_list, corr_list)])/len(dist_list)
    coeff = cd_cov/(math.sqrt(dist_var)*math.sqrt(corr_var))

    ## linear prediction fit line
    linear_pred = (lambda x: corr_mean - (cd_cov/dist_var)*dist_mean + (cd_cov/dist_var)*x)

    test_x = [0,250,300]
    test_y = [linear_pred(x) for x in test_x]
    ax.text(test_x[1], test_y[1], f"R = {coeff}", color="black", fontsize=12, ha="left", va="bottom")
    plt.title("Inter-Observation Station Observed Temperature Spatial Coupling")
    plt.plot(dist_list, corr_list, '.')
    plt.plot(test_x, test_y, color="red")
    ax.set_xlabel("Station Separation (Miles)")
    ax.set_ylabel("Station Temperature Correlation (No Unit)")
    fig.canvas.manager.set_window_title("spatial coupling")
    plt.show(block=False)
breakpoint()