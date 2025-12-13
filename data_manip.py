import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os

folder = "./oh_weather_data_raw"
for file in os.listdir(folder):
    sample = pd.read_csv(folder+'/'+file)
    tobs = sample[sample["datatype"] == "TOBS"] 
    tmax = sample[sample["datatype"] == "TMAX"]
    tmin = sample[sample["datatype"] == "TMIN"]
    date_format = "%Y-%m-%d"
    dateobj = [dt.datetime.fromisoformat(x) for x in tobs["date"]]
    dates = [x.strftime(date_format) for x in dateobj]
    breakpoint()
    plt.title(file)
    plt.plot(dates, tobs["value"], '.')
    print(dates[0])
plt.show()