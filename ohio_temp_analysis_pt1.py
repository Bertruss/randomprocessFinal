import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import math
import os
import bisect
import pickle

folder = "./data/ohio_weather_data_rev2"
date_format = "%Y-%m-%d"

# date/value lookup function, binary search tree
def value_for_date(data, target_date):
    dates = [x for x,_ in data]
    i = bisect.bisect_left(dates, target_date)
    return data[i][1] if i < len(data) and dates[i] == target_date else None

def value_for_date_fast(data, dates, target_date):
    i = bisect.bisect_left(dates, target_date)
    return data[i][1] if i < len(data) and dates[i] == target_date else None


# Generate date range indpendent of set coverage
oneday = dt.timedelta(days=1)
date_list = [dt.datetime(1990, 1, 1)] 
while date_list[-1] != dt.datetime(2025, 12, 1):
    date_list.append(date_list[-1]+oneday)

# flatten all datasets, averages temp in accordance with standard practices (min-max)/2
filedata = []
for file in os.listdir(folder):
    sample = pd.read_csv(folder+'/'+file)
    tmax = sample[sample["datatype"] == "TMAX"] 
    tmin = sample[sample["datatype"] == "TMIN"] 
    
    ## Apparently you can not rely on files having both tmax AND tmin for any given date
    # assemble list of synced max/min pairs UGH >:C
    dateobj_min = [dt.datetime.fromisoformat(x) for x in tmin["date"]]
    dateobj_max = [dt.datetime.fromisoformat(x) for x in tmax["date"]]
    dateobj = [dt.datetime.fromisoformat(x) for x in sample["date"].unique()]
    vals_min = [(x,y) for x,y in zip(dateobj_min, tmin["value"].tolist())]
    vals_max = [(x,y) for x,y in zip(dateobj_max, tmax["value"].tolist())]
    
    date_list = []
    vals_list = []
    N = 0
    for date in dateobj:
        tmax_tmp = value_for_date_fast(vals_max, dateobj_max, date)
        tmin_tmp = value_for_date_fast(vals_min, dateobj_min, date)
        if tmin_tmp != None and tmax_tmp != None:
            date_list.append(date)
            vals_list.append((tmax_tmp,tmin_tmp))
        else:
            if (tmin_tmp == None) ^ (tmax_tmp == None):
               N+=1
    day_ave = [((ma+mi)/2)/10 for ma, mi in vals_list] # divide by ten because data is stored as tenths of a degree C
    tlist = [(date, temp) for date, temp in zip(date_list, day_ave)]
    filedata.append(tlist)

# From the total set of date-value pairs, select all values that correspond to every date and generate an average
daily_ave = []
daily_var = []
daily_dev = []
daily_skew = []
for date in date_list:
    print(date)
    try:
        temp = [value_for_date(file, date) for file in filedata]
        temp = [x for x in temp if x != None]
        if None in temp:
            breakpoint()
        ave = (sum(temp)/len(temp))
        var = sum([((x-ave)**2)for x in temp])/(len(temp)-1) # N-1, "bessels correction", essentially lessens the bias towards the mean a real sample set will have 
        std_dev = math.sqrt(var)
        skew = sum([(((x-ave)/std_dev)**3)for x in temp])/(len(temp))
        daily_ave.append(ave)
        daily_var.append(var)
        daily_dev.append(std_dev)
        daily_skew.append(skew)
    except:
        breakpoint()

ohio_average_temp = {
    "date" : date_list,
    "tave" : daily_ave,
    "var" : daily_var,
    "stddev" : daily_dev,
    "skew" : daily_skew
}

# generate monthly average
monthly_ave = []
monthly_var = []
monthly_dev = []
monthly_skew =[]
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
        std_dev = math.sqrt(var)
        skew = sum([(x-ave)**3 for x in accum])/((len(accum) - 1)*math.sqrt(var)**3)
        monthly_var.append(var)
        monthly_dev.append(std_dev)
        monthly_skew.append(skew)
        accum = []
        days = 0
    temp = [value_for_date(file, date) for file in filedata]
    temp = [x for x in temp if x != None]
    if None in temp:
        breakpoint()
    accum += temp
    days += 1

ohio_monthly_temp = {
    "date" : month_date,
    "tave" : monthly_ave,
    "var"  : monthly_var,
    "stddev"  : monthly_dev,
    "skew"  : monthly_skew
}



## generate singular daily average for representative year
ave = []
var = []
dev = []
skew =[]

# Generate date range to span 1 year
oneday = dt.timedelta(days=1)
date_list = [dt.datetime(1990, 1, 1)] 
while date_list[-1] != dt.datetime(1990, 12, 31):
    date_list.append(date_list[-1]+oneday)

# Note: ignoring leap days because ehhhh :/
date_aligned_dataset = []
for i, date in enumerate(date_list):
    temp = [date_val[1] for file in filedata for date_val in file if date_val[0].day == date.day and date_val[0].month == date.month]
    date_aligned_dataset.append(temp)
    print(date.month, date.day)
    aave = sum(temp)/len(temp)
    avar = sum([((x-aave)**2)for x in temp])/(len(temp)-1)
    astd_dev = math.sqrt(avar)
    askew = sum([(x-aave)**3 for x in temp])/((len(temp) - 1)*astd_dev**3)

    ave.append(aave)        
    var.append(avar)
    dev.append(astd_dev)
    skew.append(askew)

ohio_typical_year_temp = {
    "date" : date_list,
    "tave" : ave,
    "var"  : var,
    "stddev"  : dev,
    "skew"  : skew
}


breakpoint()

m_tmp = pd.DataFrame(ohio_monthly_temp)
m_tmp.to_csv("ohio_monthly_tave_1990_2025.csv")

tmp = pd.DataFrame(ohio_average_temp)
tmp.to_csv("ohio_daily_tave_1990_2025.csv")

tmp = pd.DataFrame(ohio_typical_year_temp)
tmp.to_csv("ohio_ave_year_1990_2025.csv")

results_pt1 = {
    "ohio_typical_year_temp": ohio_typical_year_temp,
    "ohio_monthly_temp": ohio_monthly_temp,
    "ohio_average_temp": ohio_average_temp,
    "date_aligned_dataset" : date_aligned_dataset
}

with open("results_pt1.pkl", "wb") as f:
    pickle.dump(results_pt1, f, protocol=pickle.HIGHEST_PROTOCOL)

