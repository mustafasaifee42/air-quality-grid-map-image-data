import matplotlib.pyplot as plt
from netCDF4 import Dataset
import math
from mpl_toolkits.basemap import Basemap, cm
import numpy as np
import matplotlib as mpl
from matplotlib.patches import Polygon

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

plt.figure(figsize=(10, 5), dpi=144)
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

print("Creating Map...")


for i in range(0,len(airQ_list[0])):
    for k in range(0,len(airQ_list[0][i])):
        if math.isnan(airQ_list[0][i][k]):
            x = 0
        else:
            print(round(np_lat[i].item(),2), round(np_lon[k].item(),2))
            lats = [ round(np_lat[i].item() - 0.05,2), round(np_lat[i].item() + 0.05,2), round(np_lat[i].item() + 0.05,2), round(np_lat[i].item() - 0.05,2) ]
            lons = [ round(np_lon[k].item() - 0.05,2), round(np_lon[k].item() - 0.05,2), round(np_lon[k].item() + 0.05,2), round(np_lon[k].item() + 0.05,2) ]
            draw_screen_poly1(lats, lons, m, round(airQ_list[0][i][k], 2))

print("Saving Map...")

plt.savefig('airQualityHealthMap.png', transparent=True, bbox_inches='tight',pad_inches=0)