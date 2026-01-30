import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os
from collections import defaultdict
import pickle
import math
import matplotlib.dates as mdates

with open("e_data_prepped.pkl", "rb") as f:
    data = pickle.load(f)

with open("e_data_basic.pkl", "rb") as f:
    data_basic_analysis = pickle.load(f)


fueltypelist = ["AOR", "COW", "FOS", "HYC", "NG", "PET", "TSN", "WND", "NUC"]
fueltypeDesc = ["all renewables","all coal products","fossil fuels","conventional hydroelectric","natural gas","petroleum","solar","wind","nuclear"]

sectorList = ["All Sectors", "Residential", "All Commercial", "All Industrial", "Electric Utility"]
sectorListID = [99, 8, 96, 97, 1]

fuel_data = data["data"]

"""
period - YYYY-MM
costPerBtu - dollars per million Btu
generation - thousand megawatthours
totalConsumption
totalConsumptionUnits
"""
format = "%Y-%m"

r = input("Render Generation summary plot?")
if r == 'y':
    # plot all fuel types only the "All Sectors" set
    plt.title("Electric Generation Overview")
    excl = ["AOR", "FOS"] # excluding aggregate types
    for i, fuel in enumerate(fueltypelist):
        if(fuel not in excl):
            temp = fuel_data[fuel][99]
            dates = [pd.to_datetime(s, format="%Y-%m") for s in temp["period"]]
            vals = temp["generation"]
            plt.plot(dates, vals, label=fueltypeDesc[i])
            ax = plt.gca()
            #ax.xaxis.set_major_locator(mdates.MonthLocator())
            #ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))

            ax.set_xlabel("Year")
            ax.set_ylabel("Generation (1k MWhrs)")
            ax.autoscale(axis="y", tight=True)
            ax.autoscale(axis="x", tight=True)
    plt.show(block=False)
    plt.legend(loc="best", framealpha=0.9)
    fig = plt.gcf()
    fig.canvas.manager.set_window_title("Electric Generation Overview")

r = input("Render Generation summary plot (non-fossil focus)?")
if r == 'y':
    # plot all fuel types only the "All Sectors" set
    plt.title("Electric Generation Overview (Non-Fossil)")
    excl = ["AOR", "FOS", "NG", "PET", "COW"] # excluding fossil and aggregate types
    for i, fuel in enumerate(fueltypelist):
        if(fuel not in excl):
            temp = fuel_data[fuel][99]
            dates = [pd.to_datetime(s, format="%Y-%m") for s in temp["period"]]
            vals = temp["generation"]
            plt.plot(dates, vals, label=fueltypeDesc[i])
            ax = plt.gca()
            #ax.xaxis.set_major_locator(mdates.MonthLocator())
            #ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))

            ax.set_xlabel("Year")
            ax.set_ylabel("Generation (1k MWhrs)")
            ax.autoscale(axis="x", tight=True)
    plt.show(block=False)
    plt.legend(loc="upper left", framealpha=0.9)
    fig = plt.gcf()
    fig.canvas.manager.set_window_title("Electric Generation Overview Non Fossil")

mean_color = "#4C72B0"   # muted blue
mode_color = "#55A868"   # muted green
std_color  = "#DD8452"   # muted orange
scatter_color = "#c8fcbd" #"#d4cda9"

mean1_color = "#4C72B0"   # muted blue
mean2_color = "#55A868"   # muted green

std1_color  = "#AFC4E8"   # light blue fill
std2_color  = "#A9D9B6"   # light green fill

r = input("Render Generation-per-source yearly summary plot?")
if r == 'y':
    for i, data in enumerate(data_basic_analysis["basic_analysis"]):
        mean = data["mean"]
        var = data["var"]
        dev = data["dev"]
        skew = data["skew"]
        dates = data["date"] 
        modeish = [a - c*b for a, b, c in zip(mean, dev, skew)]
        maxave_1 = [m + x*1  for x, m in zip(dev, mean)]
        minave_1 = [m - x*1  for x, m in zip(dev, mean)]
        maxave_2 = [m + x*2  for x, m in zip(dev, mean)]
        minave_2 = [m - x*2  for x, m in zip(dev, mean)]
        maxave_3 = [m + x*3  for x, m in zip(dev, mean)]        
        minave_3 = [m - x*3  for x, m in zip(dev, mean)]

        fig, ax = plt.subplots()

        plt.plot(dates,mean,color=mean_color,linewidth=2,label="Mean")

        # ±3σ shaded regions
        plt.fill_between( dates, maxave_3, minave_3, color=std_color, alpha=0.25, linewidth=0, label="±3σ from mean")
        plt.fill_between( dates, maxave_2, minave_2, color=std_color, alpha=0.18, linewidth=0)
        plt.fill_between(dates,maxave_1,minave_1,color=std_color,alpha=0.12,linewidth=0)
        
        plt.title(f"Typical Ohio Year - {fueltypeDesc[i]}")
        plt.grid()
        plt.legend(loc="best", framealpha=0.9)
        #plt.margins(x=0)

        ax = plt.gca()
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))

        ax.set_xlabel("Month")
        ax.set_ylabel("Generation (1k MWhrs)")
        ax.autoscale(axis="x", tight=True)
        ax.set_ylim(bottom=0)

        plt.show(block=False)
        fig = plt.gcf()
        fig.canvas.manager.set_window_title(f"Typical Ohio Year - {fueltypeDesc[i]}")

date_list = data_basic_analysis["date_list"]
com_moments = data_basic_analysis["com_moments"]
com_price_mean = com_moments["com_price_mean"]
com_price_var = com_moments["com_price_var"]
com_price_std = com_moments["com_price_std"]
com_sales_mean = com_moments["com_sales_mean"]
com_sales_var = com_moments["com_sales_var"]
com_sales_std = com_moments["com_sales_std"]

res_moments = data_basic_analysis["res_moments"]
res_price_mean = res_moments["res_price_mean_list"]
res_price_var = res_moments["res_price_var_list"]
res_price_std = res_moments["res_price_std_list"]
res_sales_mean = res_moments["res_sales_mean_list"]
res_sales_var = res_moments["res_sales_var_list"]
res_sales_std = res_moments["res_sales_std_list"]


r = input("Render cost-supply plots?")
if r == 'y':
    
    ##### Com 
    # code re-use
    mean = com_price_mean
    var = com_price_var
    dev = com_price_std
    dates = date_list 

    maxave_3 = [m + x*3  for x, m in zip(dev, mean)]        
    minave_3 = [m - x*3  for x, m in zip(dev, mean)]
    
    fig, ax = plt.subplots()
    ax2 = ax.twinx()

    ax.plot( dates, mean, color=mean1_color, linewidth=2, label="Cost Mean")

    # ±3σ shaded regions
    ax.fill_between( dates, maxave_3, minave_3, color=std1_color, alpha=0.5, linewidth=0, label="±3σ from cost mean")

    
    plt.title(f"Typical Ohio Year - Commercial Price and Supply")
    #plt.margins(x=0)

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.set_xlabel("Month")
    ax.set_ylabel("cents per KWhr")
    ax.autoscale(axis="x", tight=True)
    ax.set_ylim(bottom=0)
    

    ## Com supply
    # code re-use
    mean = com_sales_mean
    var = com_sales_var
    dev = com_sales_std
    
    maxave_3 = [m + x*3  for x, m in zip(dev, mean)]        
    minave_3 = [m - x*3  for x, m in zip(dev, mean)]

    plt.plot(dates, mean, color=mean2_color, linewidth=2, label="Supply Mean")

    # ±3σ shaded regions
    plt.fill_between( dates, maxave_3, minave_3, color=std2_color, alpha=0.5, linewidth=0, label="±3σ from supply mean")

    #plt.margins(x=0)

    ax2.set_ylabel("Generation (Million KWhrs)")
    ax2.autoscale(axis="x", tight=True)
    ax2.set_ylim(bottom=0)

    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc="lower right", framealpha=0.9)
    ax.grid()
    plt.show(block=False)
    fig.canvas.manager.set_window_title(f"Typical Ohio Year - Commercial Price and Supply")

    ###### Res
    # code re-use
    mean = res_price_mean
    var = res_price_var
    dev = res_price_std
    dates = date_list 

    maxave_3 = [m + x*3  for x, m in zip(dev, mean)]        
    minave_3 = [m - x*3  for x, m in zip(dev, mean)]
    
    fig, ax = plt.subplots()
    ax2 = ax.twinx()

    ax.plot( dates, mean, color=mean1_color, linewidth=2, label="Cost Mean")

    # ±3σ shaded regions
    ax.fill_between( dates, maxave_3, minave_3, color=std1_color, alpha=0.5, linewidth=0, label="±3σ from cost mean")

    
    plt.title(f"Typical Ohio Year - residential Price and Supply")
    #plt.margins(x=0)

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.set_xlabel("Month")
    ax.set_ylabel("cents per KWhr")
    ax.autoscale(axis="x", tight=True)
    ax.set_ylim(bottom=0)
    

    ## res supply
    # code re-use
    mean = res_sales_mean
    var = res_sales_var
    dev = res_sales_std
    
    maxave_3 = [m + x*3  for x, m in zip(dev, mean)]        
    minave_3 = [m - x*3  for x, m in zip(dev, mean)]

    plt.plot(dates, mean, color=mean2_color, linewidth=2, label="Supply Mean")

    # ±3σ shaded regions
    plt.fill_between( dates, maxave_3, minave_3, color=std2_color, alpha=0.5, linewidth=0, label="±3σ from supply mean")

    
    #plt.margins(x=0)

    ax2.set_ylabel("Generation (Million KWhrs)")
    ax2.autoscale(axis="x", tight=True)
    ax2.set_ylim(bottom=0)
    ax.grid()
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc="lower right", framealpha=0.9)
    plt.show(block=False)
    fig.canvas.manager.set_window_title(f"Typical Ohio Year - Residential Price and Supply")
    
breakpoint()



