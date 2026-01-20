import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

#counties = gpd.read_file(".map/ne_10m_admin_2_counties/ne_10m_admin_2_counties.shp"),
#states = gpd.read_file("./map/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp")
#breakpoint()
# Load built-in world boundaries
layers = {
"A" : gpd.read_file("./map/ne_10m_admin_0_countries_usa.shp"),
"B" : gpd.read_file("./map/ne_10m_admin_2_counties.shp"),
"D" : gpd.read_file("./map/ne_10m_admin_2_counties_lines.shp"),
"H" : gpd.read_file("./map/ne_10m_roads_north_america.shp"),
"I" : gpd.read_file("./map/ne_10m_admin_1_states_provinces.shp"),
"J" : gpd.read_file("./map/ne_10m_lakes_north_america.shp"),
"K" : gpd.read_file("./map/ne_10m_lakes.shp")
}

fig, ax = plt.subplots(figsize=(12, 8))

layers["A"].plot(
    ax=ax,
    color="#f5ead5",
    edgecolor="none"
)

layers["B"].plot(
    ax=ax,
    color="#bab6ad",
    edgecolor="black"
)


layers["D"].plot(
    ax=ax,
    color="#bab6ad",
    edgecolor="black",
    alpha = .5
)

layers["H"].plot(
    ax=ax,
    color="#80808F",
    edgecolor="none",
    alpha = .2
)

layers["I"].plot(
    ax=ax,
    color="#808080",
    edgecolor="black"
)

layers["J"].plot(
    ax=ax,
    color="#aecae8",
    edgecolor="none"
)

layers["K"].plot(
    ax=ax,
    color="#aecae8",
    edgecolor="none"
)

ax.set_axis_off()

stations = pd.read_csv("./helper scripts/stations_list_rev3.csv")
for point in stations.iterrows():
    ax.scatter(point[1]["lon"], point[1]["lat"], color="#fa5a48")
    name = (point[1]["name"].split(',')[0]).title() # formatting name
    plt.annotate(
        name,
        xy=(point[1]["lon"], point[1]["lat"]),
        xytext=(point[1]["lon"], point[1]["lat"] + 0.03), # Offset text slightly from the point
        #arrowprops=dict(facecolor='black', arrowstyle='->', connectionstyle="arc3,rad=0.2"),
        fontsize = 7,
        color = "black",
        ha='center' # Horizontal alignment
    )
plt.show()


input()