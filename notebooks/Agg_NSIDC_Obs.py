
# coding: utf-8

# In[1]:


'''

This code is part of the SIPN2 project focused on improving sub-seasonal to seasonal predictions of Arctic Sea Ice. 
If you use this code for a publication or presentation, please cite the reference in the README.md on the
main page (https://github.com/NicWayand/ESIO). 

Questions or comments should be addressed to nicway@uw.edu

Copyright (c) 2018 Nic Wayand

GNU General Public License v3.0


'''

import numpy as np
import numpy.ma as ma
import os
import xarray as xr
import glob
import datetime

from esio import EsioData as ed

import dask
# from dask.distributed import Client


# In[2]:



# c = Client()
# c


# In[3]:


cd = datetime.datetime.now()
cy = cd.year
#cd = datetime.datetime(cy, 1, 2)  # force it for checking

print(cd)
firstfive = False
if ((cd.month == 1) & (cd.day<6)):
    firstfive = True
firstfive


# In[4]:


# Dirs
E = ed.EsioData.load()
data_dir = E.obs_dir

# Flags
UpdateAll = False

# Products to import
product_list = ['NSIDC_0081', 'NSIDC_0079', 'NSIDC_0051']

# Loop through each product
for c_product in product_list:
    print('Aggregating ', c_product, '...')

    for cyear in np.arange(1979,cy+1,1):
        #print(cyear)
        
        cyear_str = str(cyear)
        
        out_dir = os.path.join(data_dir, c_product, 'sipn_nc_yearly')
        if not os.path.exists(out_dir):
                os.makedirs(out_dir)
                
        nc_out = os.path.join(out_dir, cyear_str+'.nc')
        # Don't update file if exits, unless current year or in first 5 days of new year
        if ((os.path.isfile(nc_out)) & (cyear<cy-1)):
            print('Year ',cyear,' is done')
            continue
        if ((os.path.isfile(nc_out)) & ((cyear==cy-1) & (not(firstfive)))):
            print('Not first few days of year so do not redo',cyear)
            continue

        # Load in Obs
        c_files = sorted(glob.glob(E.obs[c_product]['sipn_nc']+'/*_'+cyear_str+'*.nc'))
        if len(c_files)==0:
            #print("No files found for current year")
            continue
        ds_year = xr.open_mfdataset(c_files, 
                                      concat_dim='time', parallel=True)

        print('writing netcdf file')
        ds_year.to_netcdf(nc_out)
        print(cyear)
      
    # For each Product
    print("Finished ", c_product)
    print("")


# In[5]:


ds_year = None

