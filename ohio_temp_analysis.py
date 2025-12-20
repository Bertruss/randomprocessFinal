import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os

folder = "./data/oh_weather_data"
date_format = "%Y-%m-%d"

# Generate date range indpendent of set
oneday = dt.timedelta(days=1)
date_list = [dt.datetime(1990, 1, 1)] 
while date_list[-1] != dt.datetime(2025, 12, 1):
    date_list.append(date_list[-1]+oneday)

# flatten all datasets observed temperatures
filedata = []
for file in os.listdir(folder):
    sample = pd.read_csv(folder+'/'+file)
    tobs = sample[sample["datatype"] == "TOBS"] 
    tmax = sample[sample["datatype"] == "TMAX"] # unused
    tmin = sample[sample["datatype"] == "TMIN"] # unused
    dateobj = [dt.datetime.fromisoformat(x) for x in tobs["date"]]
    
    tobs_list = [(date, temp) for date, temp in zip(dateobj, tobs["value"])]
    filedata.append(tobs_list)

# From the total set of date-value pairs, select all values that correspond to every date and generate an average
daily_ave = []
for date in date_list:
    temp = [date_val[1] for file in filedata for date_val in file if date_val[0] == date]
    daily_ave.append((sum(temp)/len(temp))/10)

ohio_average_temp = {
    "date" : date_list,
    "tave" : daily_ave
}

# generate monthly average
monthly_ave = []
month_date = []
curr_month = 1
accum = 0
days = 0
for i, val in enumerate(daily_ave):
    if not curr_month == date_list[i].month:
        print(curr_month, days)
        curr_month = date_list[i].month
        month_date.append(date_list[i-1])
        monthly_ave.append(accum/days)
        accum = 0
        days = 0
    accum += val
    days += 1 

ohio_monthly_temp = {
    "date" : month_date,
    "tave" : monthly_ave
}
breakpoint()

m_tmp = pd.DataFrame(ohio_monthly_temp)
m_tmp.to_csv("ohio_monthly_tave_1990_2025.csv")

tmp = pd.DataFrame(ohio_average_temp)
tmp.to_csv("ohio_daily_tave_1990_2025.csv")