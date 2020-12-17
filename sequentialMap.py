import numpy as np
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm
import matplotlib as mpl
import matplotlib.patches as patches
import matplotlib.colors as mcolors
from matplotlib.patches import Polygon
import json

with open('airQualityData.json') as f:
    data = json.load(f)

plt.figure(figsize=(50, 25), dpi=300)
plt.axis("off")
m = Basemap(projection='merc',llcrnrlat=-85,urcrnrlat=85,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')

# lat, lon = np.meshgrid(latitudes,longitudes)

#x,y = m(lon,lat)

m.drawcoastlines(linewidth=0,color="white", zorder=1)
def draw_screen_poly1( lats, lons, m,clr):
    x1,y1 = m(lons[0],lats[0])
    x2,y2 = m(lons[1],lats[1])
    x3,y3 = m(lons[2],lats[2])
    x4,y4 = m(lons[3],lats[3])
    poly = Polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)],facecolor=clr,alpha=1)
    plt.gca().add_patch(poly)

def hex_to_rgb(value):
    '''
    Converts hex to rgb colours
    value: string of 6 characters representing a hex colour.
    Returns: list length 3 of RGB values'''
    value = value.strip("#") # removes hash symbol if present
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_dec(value):
    '''
    Converts rgb to decimal colours (i.e. divides each value by 256)
    value: list (length 3) of RGB values
    Returns: list (length 3) of decimal values'''
    return [v/256 for v in value]


def get_continuous_cmap(hex_list, float_list=None):
    ''' creates and returns a color map that can be used in heat map figures.
        If float_list is not provided, colour map graduates linearly between each color in hex_list.
        If float_list is provided, each color in hex_list is mapped to the respective location in float_list. 
        
        Parameters
        ----------
        hex_list: list of hex code strings
        float_list: list of floats between 0 and 1, same length as hex_list. Must start with 0 and end with 1.
        
        Returns
        ----------
        colour map'''
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

for el in data["data"]:
    lats = [ round(el['lat'] - 0.05,2), round(el['lat'] + 0.05,2), round(el['lat'] + 0.05,2), round(el['lat'] - 0.05,2) ]
    lons = [ round(el['lon'] - 0.05,2), round(el['lon'] - 0.05,2), round(el['lon'] + 0.05,2), round(el['lon'] + 0.05,2) ]
    draw_screen_poly1( lats, lons, m, cmap(norm(el['value']))  )

print("Saving Map...")

plt.savefig('airQualitySequentialMap.png', transparent=True, bbox_inches='tight',pad_inches=0)