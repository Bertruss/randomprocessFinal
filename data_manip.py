import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os

folder = "./oh_data"
for file in os.listdir(folder):
    print(file)
    sample = pd.read_csv(folder+'/'+file)
    tobs = sample[sample["datatype"] == "TOBS"] 
    tmax = sample[sample["datatype"] == "TMAX"]
    tmin = sample[sample["datatype"] == "TMIN"]
    date_format = "%Y-%m-%d"
    dateobj = [dt.datetime.fromisoformat(x) for x in tobs["date"]]
    dates = [x.strftime(date_format) for x in dateobj]
    
    #plt.title(file)
    plt.plot(dateobj, tobs["value"], '.')
    breakpoint()
plt.show()