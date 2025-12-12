import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime as dt

test = pd.read_csv("weather_data_ohio_1990_2025.csv")

## separating out data sources
Data_locales = test["NAME"].unique()
date_format = "%Y-%m-%d"
Mansfield = test[test["NAME"] == Data_locales[0]]
temp = Mansfield["DATE"]
Mansfield_dates = [dt.strptime(x, date_format) for x in temp]
#plt.plot(Mansfield_dates, Mansfield["TAVG"], '.')
#plt.show()