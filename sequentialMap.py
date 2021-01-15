import numpy as np
from netCDF4 import Dataset
import math
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm
import matplotlib as mpl
import matplotlib.patches as patches
import matplotlib.colors as mcolors
from matplotlib.patches import Polygon
from datetime import datetime


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

plt.figure(figsize=(25, 12.5), dpi=300)
plt.axis("off")
m = Basemap(projection='merc',llcrnrlat=-85,urcrnrlat=85,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')

m.drawcoastlines(linewidth=0,color="white", zorder=1)
def draw_screen_poly1( lats, lons, m,clr):
    x1,y1 = m(lons[0],lats[0])
    x2,y2 = m(lons[1],lats[1])
    x3,y3 = m(lons[2],lats[2])
    x4,y4 = m(lons[3],lats[3])
    poly = Polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)],facecolor=clr,alpha=1)
    plt.gca().add_patch(poly)


def hex_to_rgb(value):
    value = value.strip("#")
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_dec(value):
    return [v/256 for v in value]


def get_continuous_cmap(hex_list, float_list=None):
    rgb_list = [rgb_to_dec(hex_to_rgb(i)) for i in hex_list]
    if float_list:
        pass
    else:
        float_list = list(np.linspace(0,1,len(rgb_list)))
        
    cdict = dict()
    for num, col in enumerate(['red', 'green', 'blue']):
        col_list = [[float_list[i], rgb_list[i][num], rgb_list[i][num]] for i in range(len(float_list))]
        cdict[col] = col_list
    cmp = mcolors.LinearSegmentedColormap('my_cmp', segmentdata=cdict, N=256)
    return cmp
    
norm = mpl.colors.Normalize(vmin=0, vmax=300)
hex_list = ['#009966','#ffde33','#ff9933','#cc0033','#660099','#7e0023','#0d0000']
float_list=[0, norm(12), norm(35.5), norm(55.5), norm(150.5), norm(250.5), 1]
cmap  = get_continuous_cmap(hex_list, float_list)

print("Creating Map...")


now1 = datetime.now()

current_time = now1.strftime("%H:%M:%S")
print("Current Time =", current_time)

for i in range(0,len(airQ_list[0])):
    for k in range(0,len(airQ_list[0][i])):
        if math.isnan(airQ_list[0][i][k]):
            x = 0
        else:
            lats = [ round(np_lat[i].item() - 0.05,2), round(np_lat[i].item() + 0.05,2), round(np_lat[i].item() + 0.05,2), round(np_lat[i].item() - 0.05,2) ]
            lons = [ round(np_lon[k].item() - 0.05,2), round(np_lon[k].item() - 0.05,2), round(np_lon[k].item() + 0.05,2), round(np_lon[k].item() + 0.05,2) ]
            draw_screen_poly1( lats, lons, m, cmap(norm(round(airQ_list[0][i][k], 2)))  )

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
print("Ellapsed Time =", now - now1)

print("Saving Map...")

plt.savefig('airQualitySequentialMap1.png', transparent=True, bbox_inches='tight',pad_inches=0)
now2 = datetime.now()

current_time = now2.strftime("%H:%M:%S")
print("Current Time =", current_time)
print("Ellapsed Time =", now2 - now)
print("Ellapsed Time Total =", now2 - now1)
plt.close()