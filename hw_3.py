# This script downloads netCDF data from URL and creates ba map of 
# Daily averaged outgoing longwave radiation of Gulf of Mexico
# and East coast.

# Created by: Arjun Adhikari
# TAMUG

## PART 1
###############################################

import netCDF4
from datetime import datetime
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = netCDF4.Dataset('http://apdrc.soest.hawaii.edu:80/dods/public_data/satellite_product/OLR/olr_daily')

time = data.variables['time']
rad = data.variables['olr'][0,:]
lon = data.variables['lon'][:]
lat = data.variables['lat'][:]
lon,lat = np.meshgrid(lon,lat)

mm = Basemap(llcrnrlon=-100,llcrnrlat=25,urcrnrlon=-60,urcrnrlat=55,projection='lcc',resolution='l',lat_0=40,lon_0=-80)
x,y = mm(lon,lat)

mm.drawmapboundary(color='k')
mm.drawcoastlines()        
mm.fillcontinents(lake_color='white') 
mm.drawcoastlines(linewidth = 0.3)
mm.drawmeridians(np.arange(-100,-60,10),labels=[1,0,0,1],fontsize=10)
mm.drawparallels(np.arange(30,55,10),labels=[1,0,0,1],fontsize=10)

cmap = plt.cm.jet
mm.pcolormesh(x,y,rad,shading='flat',cmap=cmap)
cb = mm.colorbar()
plt.title('Satellite Observed Daily Averaged Outgoing Longwave Radiation [$W / m^2$]',fontsize=14,style='italic')
plt.show()
plt.savefig('Qlw_plan_view_Homework_3.png')
plt.close("all")

################################################
# PART 2: CREATING PANDAS TIME-SERIES
################################################

from matplotlib.dates import num2date, epoch2num

time = data.variables['time'][:]
rad = data.variables['olr'][:,0,10]
rng = pd.date_range('1/6/1974', periods=rad.size, freq='D')
ts = pd.Series(rad,index=rng)
series = pd.DataFrame(ts)

series.plot(figsize=(11.0, 7.0),legend = False)
plt.title('Daily Mean Time series of Outgoing Longwave Radiation [$W / m^2$] from 01Jun1974 to 31Dec2012.', fontsize =14 , style ='italic')
plt.xlabel('Time [Year]',fontsize =12)
plt.ylabel('Daily Mean [$W / m^2$]',fontsize =12)
plt.show()
plt.savefig('Time_Series.png')