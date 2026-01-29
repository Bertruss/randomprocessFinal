import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import os
from collections import defaultdict
import pickle
import math
file = "./data/analysis_set/ohio_electrical_data_1990_2025.csv"
e_sample = pd.read_csv(file)
dformat="%Y-%m"

def has_any_nonzero(arr):
    arr = np.asarray(arr)
    return np.nanmax(np.abs(arr)) > 0 if not np.all(np.isnan(arr)) else False

## Breaking down monolithic electrical dataset into parsable 

# sync fuel types and fuel type description
fuel_types = e_sample["fueltypeid"].tolist()
idx = defaultdict(list)
for i, x in enumerate(fuel_types):
    idx[x].append(i)
unique_indices = [v[0] for v in idx.values()]

ftl = []
fdl = []
for i in unique_indices:
    ftl.append(e_sample["fueltypeid"][i])
    fdl.append(e_sample["fuelTypeDescription"][i])


# energy sectors synced with IDs
sect_id = e_sample["sectorid"].tolist()
idx = defaultdict(list)
for i, x in enumerate(sect_id):
    idx[x].append(i)
unique_indices = [v[0] for v in idx.values()]

sid = []
sdl = []
for i in unique_indices:
    sid.append(e_sample["sectorid"][i])
    sdl.append(e_sample["sectorDescription"][i])

# selecting a smaller dataset
subfueltypelist = ["AOR", "COW", "FOS", "HYC", "NG", "PET", "SUN", "WND", "NUC", "TSN"]
subsectorList = ["All Sectors", "Residential", "All Commercial", "All Industrial", "Electric Utility"]
subsectorListID = [99, 8, 96, 97, 1]

# breaking data down by fuel type. 
fuel_type_list = subfueltypelist
sector_ID = subsectorListID
fuel_data = dict()
for ftype in fuel_type_list:
    fuel_by_sector = dict()
    # breaking down by sector
    cost_test = []
    costPerBtu_test = []
    generation_test = []
    heatContent_test = []
    totalConsumption_test = []
    totalConsumptionUnits_test = []
    print(f"running {ftype} ###############")
    sub_sample = []
    for s_id in sector_ID:
        sub_sample = []
        sub_sample = e_sample[e_sample["fueltypeid"] == ftype]
        sub_sample = sub_sample[sub_sample["sectorid"] == s_id]
        
        period = []
        cost = []
        costPerBtu = []
        generation = []
        heatContent = []
        totalConsumption = []
        totalConsumptionUnits = []
        if sub_sample.empty:
            print(f"{ftype} None {s_id}")
        else:
            period = [val for val in sub_sample["period"]]
            cost = [val for val in sub_sample["cost"]]
            # costUnits = [val for val in sub_sample["cost-units"]]
            costPerBtu = [val for val in sub_sample["cost-per-btu"]]
            # costPerBtuUnits = [val for val in sub_sample["cost-per-btu-units"]] always dollars per million Btu
            generation = [val for val in sub_sample["generation"]]
            # generationUnits = [val for val in sub_sample["generation-units"]] always thousand megawatthours
            heatContent = [val for val in sub_sample["heat-content"]] 
            totalConsumption = [val for val in sub_sample["total-consumption"]]
            totalConsumptionUnits = [val for val in sub_sample["total-consumption-units"]]

            fuel_sector_data = {
                "period" : period,
                "cost": cost,
                "costPerBtu" : costPerBtu,
                "generation" : generation,
                "totalConsumption" : totalConsumption,
                "totalConsumptionUnits" : totalConsumptionUnits,
            }
            ## All set testing
            cost = [float(x) for x in cost if not math.isnan(x)] # filter nan
            costPerBtu = [float(x) for x in costPerBtu if not math.isnan(x)] # filter nan
            generation = [float(x) for x in generation if not math.isnan(x)] # filter nan
            heatContent = [float(x) for x in heatContent if not math.isnan(x)] # filter nan
            totalConsumption = [float(x) for x in totalConsumption if not math.isnan(x)] # filter nan
            cost_test.append(float(sum(cost)))   
            costPerBtu_test.append(float(sum(costPerBtu))) 
            generation_test.append(float(sum(generation)))
            if(float(sum(generation)) != 0.0):
               print(f"{ftype}: {s_id} Has generation data")
            heatContent_test.append(float(sum(heatContent)))    
            totalConsumption_test.append(float(sum(totalConsumption)))   
            
            fuel_by_sector[s_id] = fuel_sector_data
    # checking if ANY SECTOR has unique data or if all contain the same information
    testing = [len(set(cost_test)), len(set(costPerBtu_test)), len(set(generation_test)), len(set(heatContent_test)), len(set(totalConsumption_test))]  
    print(testing)
    fuel_data[ftype] = fuel_by_sector

## load commercial and residential delivery and price information
file = "./data/analysis_set/ohio electrical_cost_consumption_1990_2025.csv"
sale_sample = pd.read_csv(file)
salesectorid = ['RES', 'COM']
price_unit = "cents per kilowatt-hour"
sales_unit = "million kilowatt hours"

sub_sample = sale_sample[sale_sample["sector"] == 'RES']
period = sub_sample["period"].to_list()
price = sub_sample["price"].to_list()
sales = sub_sample["sales"].to_list()
res_sales = {
    "period" : period,
    "price" : price,
    "sales" : sales
}

sub_sample = sale_sample[sale_sample["sector"] == 'COM']
period = sub_sample["period"].to_list()
price = sub_sample["price"].to_list()
sales = sub_sample["sales"].to_list()
com_sales = {
    "period" : period,
    "price" : price,
    "sales" : sales
}


e_data_package = {
    "fuelType" : ftl,
    "fuelDesc" : fdl,
    "sectorID" : sid,
    "sectorDesc" : sdl,
    "data" : fuel_data,
    "res_sales" : res_sales,
    "com_sales" : com_sales,
    "price_unit" : price_unit,
    "sales_unit" : sales_unit
}

with open("e_data_prepped.pkl", "wb") as f:
    pickle.dump(e_data_package, f, protocol=pickle.HIGHEST_PROTOCOL)