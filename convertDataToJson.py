
from netCDF4 import Dataset
import numpy as np
import math
import json
from netCDF4 import num2date
import pandas as pd
import csv
import requests


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


def convert(s): 
    # initialization of string to "" 
    str1 = "" 
  
    # using join function join the list s by  
    # separating words by str1 
    return(str1.join(s)) 


strng = []
for val in nc.variables['time_string'][:]:
    strng.append(val[0].decode('UTF-8'))

obj = {"dateTime": convert(strng), "data": []}
for i in range(0,len(airQ_list[0])):
    for k in range(0,len(airQ_list[0][i])):
        if math.isnan(airQ_list[0][i][k]):
            x = 0
        else:
            d = {'lat': round(np_lat[i].item(), 2), 'lon': round(np_lon[k].item(), 2), 'value': round(airQ_list[0][i][k], 2)}
            obj["data"].append(d)

print("Saving JSON...")
with open('airQualityData.json', 'w') as f: # writing JSON object
    json.dump(obj, f, indent=4)