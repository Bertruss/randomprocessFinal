import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os

file = "./data/analysis_set/ohio_electrical_data_1990_2025.csv"
output = "./data/analysis_set/electric/"
e_sample = pd.read_csv(file)
dformat="%Y-%m"
fuel_types = e_sample["fueltypeid"].unique().tolist()
fuel_desc = e_sample["sectorDescription"].unique().tolist()
breakpoint()

output_postfix = "_ohio_electrical_1990_2025.csv"

for ftype in fuel_types:
    # select entries per fueltype
    selection = e_sample[e_sample["fueltypeid"] == ftype]
    total_power = selection[selection["sectorDescription"] == "All Sectors"]
    cost = selection[selection["sectorDescription"] == "Electric Utility"]
    dates = total_power["period"]
    total = total_power["generation"]

    # reverse sets
    dates = dates[::-1]
    total = total[::-1]

    dateobj = [dt.datetime.strptime(date, dformat) for date in dates]
    breakpoint()
    data = {
        "date": dates.to_list(),
        "1kMwH": total.to_list()
    }
    
    total_power_pd = pd.DataFrame(data)
    breakpoint()

breakpoint()