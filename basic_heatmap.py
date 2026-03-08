import pandas as pd
import glob
import matplotlib.pyplot as plt
import seaborn as sns
#from sklearn.cluster import KMeans
import contextily as cx

# load all bike datasets
files = glob.glob("data/bikes_*.csv")
df_list = [pd.read_csv(file) for file in files]

bikes = pd.concat(df_list, ignore_index=True)

# limito to only Rotterdam
lat_min, lat_max = 51.837, 51.998
lon_min, lon_max = 4.256, 4.712

bikes = bikes[
    (bikes["lat"] >= lat_min) & (bikes["lat"] <= lat_max) &
    (bikes["lon"] >= lon_min) & (bikes["lon"] <= lon_max)
]

# remove disabled bikes
bikes = bikes[bikes["is_disabled"] == False]

fig, ax = plt.subplots(figsize=(12, 10))

sns.kdeplot(
        data=bikes, 
        x="lon", 
        y="lat", 
        fill=True, 
        thresh=0.1, 
        levels=15, 
        cmap="YlOrRd", 
        alpha=0.6, 
        ax=ax
    )

# add the Rotterdam map background
cx.add_basemap(ax, crs="EPSG:4326", source=cx.providers.CartoDB.Positron)

plt.title("Bike Demand Clusters")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.show()