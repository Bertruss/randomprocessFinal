import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os
from collections import defaultdict
import pickle
import math

with open("e_data_prepped.pkl", "rb") as f:
    data = pickle.load(f)

with open("e_data_basic.pkl", "rb") as f:
    data = pickle.load(f)


fueltypelist = ["AOR", "COW", "FOS", "HYC", "NG", "PET", "SUN", "WND", "NUC"]
sectorList = ["All Sectors", "Residential", "All Commercial", "All Industrial", "Electric Utility"]
sectorListID = [99, 8, 96, 97, 1]
fuelType = data["fuelType"]
fuelDesc = data["fuelDesc"]
sectorID = data["sectorID"]
sectorDesc = data["sectorDesc"]
fuel_data = data["data"]

"""
period - YYYY-MM
costPerBtu - dollars per million Btu
generation - thousand megawatthours
totalConsumption
totalConsumptionUnits
"""
format = "%Y-%m"


# plot all fuel types only the "All Sectors" set
plt.title("Electric Generation Overview")
for fuel in fueltypelist:
    temp = fuel_data[fuel][99]
    dates = [pd.to_datetime(s, format="%Y-%m") for s in temp["period"]]
    vals = temp["generation"]
    plt.plot(dates, vals, label=fuel)
    plt.show(block=False)
breakpoint()



