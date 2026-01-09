import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os

folder = "./data/ohio_weather_data_rev2"
date_format = "%Y-%m-%d"

# list of files without usable temperature data
bad_list = []

# list of files requiring finagaling 
mid_files = []

# Generate date range indpendent of set
oneday = dt.timedelta(days=1)
date_list = [dt.datetime(1990, 1, 1)] 
while date_list[-1] != dt.datetime(2025, 12, 1):
    date_list.append(date_list[-1]+oneday)

# flatten all datasets, averages temp
filedata = []
for file in os.listdir(folder):
    sample = pd.read_csv(folder+'/'+file)
    tobs = sample[sample["datatype"] == "TOBS"] 
    tobs = sample[sample["datatype"] == "TAVG"] 
    tmax = sample[sample["datatype"] == "TMAX"] 
    tmin = sample[sample["datatype"] == "TMIN"] 
        
    dateobj = [dt.datetime.fromisoformat(x) for x in tmin["date"]]
    day_ave = [(ma-mi)/2 for mi, ma in zip(tmin["value"], tmax["value"])]
    tlist = [(date, temp) for date, temp in zip(dateobj, tmax["value"])]
    filedata.append(tlist)

# From the total set of date-value pairs, select all values that correspond to every date and generate an average
daily_ave = []
daily_var = []
for date in date_list:
    print(date)
    try:
        temp = [date_val[1] for file in filedata for date_val in file if date_val[0] == date]
        ave = (sum(temp)/len(temp))
        var = sum([((x-ave)**2)for x in temp])/(len(temp)-1)
        daily_ave.append(ave)
        daily_var.append(var)
    except:
        breakpoint()

ohio_average_temp = {
    "date" : date_list,
    "tave" : daily_ave,
    "var" : daily_var
}
breakpoint()
# generate monthly average
monthly_ave = []
monthly_var = []
month_date = []
curr_month = 1
accum = []
days = 0
for i, date in enumerate(date_list):
    if not curr_month == date_list[i].month:
        print(curr_month, days)
        curr_month = date_list[i].month
        month_date.append(date_list[i-1])
        ave = sum(accum)/len(accum)
        monthly_ave.append(ave)
        var = sum([((x-ave)**2)for x in accum])/(len(accum)-1)
        monthly_var.append(var)
        accum = []
        days = 0
    temp = [date_val[1] for file in filedata for date_val in file if date_val[0] == date]
    accum += temp
    days += 1

ohio_monthly_temp = {
    "date" : month_date,
    "tave" : monthly_ave,
    "stddev"  : monthly_var
}

# flatten years to derive statistical moments relative to their months

breakpoint()

m_tmp = pd.DataFrame(ohio_monthly_temp)
m_tmp.to_csv("ohio_monthly_tave_1990_2025.csv")

tmp = pd.DataFrame(ohio_average_temp)
tmp.to_csv("ohio_daily_tave_1990_2025.csv")