import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os

data = pd.read_csv("stations_list_rev2.csv")

# list of files without usable temperature data
bad_list = pd.read_csv("bad_list.csv")

# list of files requiring finagaling 
mid_files = pd.read_csv("mid_files.csv")

new_list = []
removed = []
for entry in data.iterrows():
    if entry[1]["id"] in mid_files["0"].to_list() or entry[1]["id"] in bad_list["0"].to_list():
        if entry[1]["id"] in mid_files["0"].to_list():
            res = "min/max only"        
        else:
            res = "no temp data"
        #remove from files_list
        temp = entry[1].to_dict()
        temp["removalReason"] = res
        removed.append(temp)
    else:
        new_list.append(entry[1].to_dict())
removed = pd.DataFrame(removed)
new_list = pd.DataFrame(new_list)
breakpoint()