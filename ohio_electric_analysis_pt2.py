import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os
from collections import defaultdict
import pickle

with open("e_data_prepped.pkl", "rb") as f:
    data = pickle.load(f)

fueltypelist = ["AOR", "BIO", "COW", "FOS", "HYC", "NG", "PET", "SUN", "WND", "ALL", "NUC"]
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

# plot all fuel types
for fuel in fueltypelist:
    for I, sector in enumerate(sectorListID):
        temp = fuel_data[fuel][99]
        dates = [pd.to_datetime(s, format="%Y-%m") for s in temp["period"]]
        cost = temp["costPerBtu"]
        vals = temp["generation"]
        fig, ax = plt.subplots()
        plt.title(f"{fuel} {sectorList[I]}")
        ax.plot(dates, vals)
        ax2 = ax.twinx()
        ax.plot(dates, cost)
        plt.show(block=False)
    breakpoint()




