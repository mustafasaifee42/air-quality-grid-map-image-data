
from netCDF4 import Dataset

import numpy as np
import math
import json
from netCDF4 import num2date
import pandas as pd
import csv
import requests
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm
import matplotlib as mpl
import matplotlib.patches as patches
import matplotlib.colors as mcolors
from matplotlib.patches import Polygon


receive = requests.get('http://berkeleyearth.lbl.gov/air-quality/data/Current_Map.nc')
with open(r'mapDataUpdated.nc','wb') as f: 
    f.write(receive.content)
    
nc = Dataset('mapDataUpdated.nc', 'r')

latitudes = nc.variables['latitude'][:]
longitudes = nc.variables['longitude'][:]
airQ = nc.variables['pm25'][:]
np_lat = np.array(latitudes)
np_lon = np.array(longitudes)
np_temp = np.array(airQ)
airQ_list = np_temp.tolist()
i=0
k=0

array = []

vMax = 0
for i in range(0,len(airQ_list[0])):
    for k in range(0,len(airQ_list[0][i])):
        if math.isnan(airQ_list[0][i][k]):
            x = 0
        else:
            d = {'lat': round(np_lat[i].item(), 2), 'lon': round(np_lon[k].item(), 2), 'value': round(airQ_list[0][i][k], 2)}
            if vMax < round(airQ_list[0][i][k], 2):
                vMax = round(airQ_list[0][i][k], 2)
            array.append(d)

plt.figure(figsize=(50, 25), dpi=300)
plt.axis("off")
m = Basemap(projection='merc',llcrnrlat=-85,urcrnrlat=85,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
m.drawcoastlines(linewidth=0,color="white", zorder=1)
def draw_screen_poly1( lats, lons, m, val):
    x1,y1 = m(lons[0],lats[0])
    x2,y2 = m(lons[1],lats[1])
    x3,y3 = m(lons[2],lats[2])
    x4,y4 = m(lons[3],lats[3]) 
    if val > 250.4:
        poly = Polygon( [(x1,y1),(x2,y2),(x3,y3),(x4,y4)], facecolor='#7e0023', alpha=1 )
        plt.gca().add_patch(poly)
    if val <= 250.4 and val > 150.4:
        poly = Polygon( [(x1,y1),(x2,y2),(x3,y3),(x4,y4)], facecolor='#660099', alpha=1 )
        plt.gca().add_patch(poly)
    if val <= 150.4 and val > 55.4:
        poly = Polygon( [(x1,y1),(x2,y2),(x3,y3),(x4,y4)], facecolor='#cc0033', alpha=1 )
        plt.gca().add_patch(poly)
    if val <= 55.4 and val > 35.4:
        poly = Polygon( [(x1,y1),(x2,y2),(x3,y3),(x4,y4)], facecolor='#ff9933', alpha=1 )
        plt.gca().add_patch(poly)
    if val <= 35.4 and val > 12:
        poly = Polygon( [(x1,y1),(x2,y2),(x3,y3),(x4,y4)], facecolor='#ffde33', alpha=1 )
        plt.gca().add_patch(poly)
    if val < 12:
        poly = Polygon( [(x1,y1),(x2,y2),(x3,y3),(x4,y4)], facecolor='#009966', alpha=1 )
        plt.gca().add_patch(poly)

for el in array:
    lats = [ round(el['lat'] - 0.05,2), round(el['lat'] + 0.05,2), round(el['lat'] + 0.05,2), round(el['lat'] - 0.05,2) ]
    lons = [ round(el['lon'] - 0.05,2), round(el['lon'] - 0.05,2), round(el['lon'] + 0.05,2), round(el['lon'] + 0.05,2) ]
    draw_screen_poly1(lats, lons, m, el['value'])


plt.savefig('airQualityHealthMap.png', transparent=True, bbox_inches='tight',pad_inches=0)