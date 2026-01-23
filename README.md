General Notes

In this paper I will be analyzing patterns and relationships between ohio weather patterns and electricity demand, capacity, and source diversity.

A period spanning from 1990 to the present (November 2025) was selected arbitrarily as a period of significant enough length to be indicative of long term trends, and it was anticipated this period would demonstrate the most significant diversification of the makeup of electrical generation sources with the state of Ohio. 

Within the dataset for weather information for the state of ohio, there are over 1900 different observation stations from which weather data has been recorded with records existing as far back as 1871. These stations were narrowed down to a list of only 75; all stations that cover the relevant period (1990-present), and containing the relevant temperature data.

figure1: locations of selected observation stations for the relevant time period (1990-present).
Map created using assets from Natural Earth using geopandas python library.

It needs to be noted that the temperature measurements are not entirely heterogeneous, and are frustratingly inconsistent. There is both the 'TOBS' datatype, which is simply observed temperature at the time of recording, then there is also the 'TAVG' datatype, where "average" is not defined by a specific calculation but is at the discretion of the administration of an individual observation station. It may be calculated by averaging a minutely or hourly temperature measurement done throughout the day, or from a series of measurements taken at a longer fixed interval. Furthermore, few if any datasets that may have this daily average have full coverage of the desired time period with this measurement. Therefore, I have opted to instead use a widely accepted method, by which the daily mean is estimated by averaging the minimum and maximum observed temperature, measurements which have very near full coverage. (https://www.climate.gov/maps-data/climate-data-primer/how-do-weather-observations-become-climate-data)

I aggregated this data together into a single "ohio" dataset, and functionally this allowed me to turn the daily temperature and monthly temperature into random variables defined by their sample mean and variance. The aggregate "daily" and "monthly" datasets are then comprised of corresponding mean, variance and skew for every available data point for every day.

figure 2: daily
figure 3: monthly
figure 4: the average ohio year

plots generated using the matplotlib library for python, which recreates MATLAB plotting functionality and API

After establishing some baseline analyses of the weather data as a whole, I thought it would be interesting to frame individual observation stations as RVs. Lets ask a simple question about the weather as it relates to these stations: What is the relationship, if any, between station covariance and the straight-line distance between them? Intuitively, a hypothesis might be that one would expect a high degree of correlation between the covariance and station-to-station distance, as local geography has an important role in weather and weather patterns themselves are spatially dependent phenomena. 

figure 5: covariance matrix
figure 6: plot of covariance to linear-distance

conclusion 