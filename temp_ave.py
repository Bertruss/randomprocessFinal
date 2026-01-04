import pandas as pd
import math
import matplotlib.pyplot as plt
import datetime as dt
import os
import statistics as st

file = "./data/oh_weather_data/USW00093812_1990_2025_redo.csv"

sample = pd.read_csv(file)

tmax = sample[sample["datatype"] == "TMAX"]
tmin = sample[sample["datatype"] == "TMIN"]
PRCP = sample[sample["datatype"] == "PRCP"]
SNOW = sample[sample["datatype"] == "SNOW"]
SNWD = sample[sample["datatype"] == "SNWD"]
TMAX = sample[sample["datatype"] == "TMAX"]
TMIN = sample[sample["datatype"] == "TMIN"]
WT01 = sample[sample["datatype"] == "WT01"]
WT06 = sample[sample["datatype"] == "WT06"]
WT03 = sample[sample["datatype"] == "WT03"]
WT08 = sample[sample["datatype"] == "WT08"]
WT02 = sample[sample["datatype"] == "WT02"]
WT16 = sample[sample["datatype"] == "WT16"]
WT14 = sample[sample["datatype"] == "WT14"]
WT18 = sample[sample["datatype"] == "WT18"]
WT17 = sample[sample["datatype"] == "WT17"]
WT04 = sample[sample["datatype"] == "WT04"]
WT15 = sample[sample["datatype"] == "WT15"]
WT09 = sample[sample["datatype"] == "WT09"]
WT13 = sample[sample["datatype"] == "WT13"]
WT21 = sample[sample["datatype"] == "WT21"]
WT22 = sample[sample["datatype"] == "WT22"]
WT11 = sample[sample["datatype"] == "WT11"]
WV01 = sample[sample["datatype"] == "WV01"]
AWND = sample[sample["datatype"] == "AWND"]
FMTM = sample[sample["datatype"] == "FMTM"]
PGTM = sample[sample["datatype"] == "PGTM"]
TAVG = sample[sample["datatype"] == "TAVG"]
WDF2 = sample[sample["datatype"] == "WDF2"]
WDF5 = sample[sample["datatype"] == "WDF5"]
WSF2 = sample[sample["datatype"] == "WSF2"]
WSF5 = sample[sample["datatype"] == "WSF5"]
WV03 = sample[sample["datatype"] == "WV03"]
WT19 = sample[sample["datatype"] == "WT19"]
TSUN = sample[sample["datatype"] == "TSUN"]
ADPT = sample[sample["datatype"] == "ADPT"]
ASLP = sample[sample["datatype"] == "ASLP"]
ASTP = sample[sample["datatype"] == "ASTP"]
AWBT = sample[sample["datatype"] == "AWBT"]

date_format = "%Y-%m-%d"
dateobj = [dt.datetime.fromisoformat(x) for x in tmax["date"].to_list()]
dates = [x.strftime(date_format) for x in dateobj]

ave = [int((max+min)/2) for max, min in zip(tmax["value"].to_list(), tmin["value"].to_list())]

dtype = ["TOBS" for x in range(len(ave))]

simplified = {
    "value": ave,
    "datatype": dtype,
    "date": dates
}

simple = pd.DataFrame(simplified)

# subset of approximated average values that correspond to recorded averages for approxarison
approx = []
for entry in TAVG.iterrows():
    date = dt.datetime.fromisoformat(entry[1]["date"]).strftime(date_format)
    val = simple[simple["date"] == date]["value"].iloc[0]
    approx.append(val)
overlap = [dt.datetime.fromisoformat(entry[1]["date"]) for entry in TAVG.iterrows()]
actual = TAVG["value"].to_list()

# verify similarity of sets
plt.ion()
plt.show()
plt.title("Comparison of average temperature approximation to actual")
plt.plot(overlap, actual, 'o', alpha=.5)
plt.plot(overlap, approx, "^", alpha=.5)
plt.pause(.5)
diff = [(b-a)/10 for a, b in zip(actual, approx)]

print("Assessing quality of approximation:")
print()
print("Mean difference between Approx. and Actual:")
print(sum(diff)/len(diff))
print()
print("Correlation Coeff between Approx. and Actual")
N = len(approx)

E_approx = sum(approx)/N
print(f"Mean Approx:{E_approx}")

E_actual = sum(actual)/N
print(f"Mean Actual:{E_actual}")
print()
norm_approx = [val-E_approx for val in approx]
norm_actual = [val-E_actual for val in actual]
cov_ac = sum([n_c*n_a for n_c,n_a in zip(norm_approx, norm_actual)])/N

var_approx = sum([x**2 for x in approx])/N - E_approx**2 
var_actual = sum([x**2 for x in actual])/N - E_actual**2

cor_ac = cov_ac/(math.sqrt(var_actual)*math.sqrt(var_approx))
print(f"Correlation Coeff Actual vs Approx:{cor_ac}")
print()
breakpoint()
simple.to_csv("./oh_data/USW00093812_1990_2025.csv")


breakpoint()