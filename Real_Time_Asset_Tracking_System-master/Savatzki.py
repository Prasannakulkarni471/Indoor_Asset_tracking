#!/usr/bin/env python
# coding: utf-8

# In[1]: Importing Libraries
from IPython import get_ipython
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as ss
import time
# get_ipython().run_line_magic('matplotlib', 'inline')

start = time.time()
# In[2]: Reading Data into Dataframe 
df = pd.read_excel(r"C:\Users\chris\Downloads\IPS trials\Trial 1.xlsx")

# In[3] Removing Unnecessary Columns 
df = df.drop(df.columns[[1,2,3,7,8]],axis=1)

# In[4] Naming The Columns
df.columns = ['SNO','Time','Beacon_Mac','rssi']

# In[5] Getting The Seconds from the timestamp
df['Time'] = pd.to_datetime(df['Time'])
df['seconds'] = (df['Time'].dt.hour)* 3600 + (df['Time'].dt.minute)*60 + (df['Time'].dt.second) 

# In[6] Filtering the whole data into data from 4 beacons
b_9D = df[df['Beacon_Mac'] == "C645C401019D"].copy()
b_A6 = df[df['Beacon_Mac'] == "C645C40101A6"].copy()
b_99 = df[df['Beacon_Mac'] == "C645C4010199"].copy()
b_80 = df[df['Beacon_Mac'] == "C645C4010180"].copy()

# In[7] Setting Polynomial Order to 3
poly_order = 3

# In[8] Making the columns of the Dataframe into a list variable 
columnb_9D = list(b_9D.columns)
columnb_A6 = list(b_A6.columns)
columnb_99 = list(b_99.columns)
columnb_80 = list(b_80.columns)

# In[9] Filtering data using Savgol filter and storing it as dictionary
filteredb_9D = {}
filteredb_A6 = {}
filteredb_99 = {}
filteredb_80 = {}

filteredb_9D[columnb_9D[3]] = ss.savgol_filter(b_9D[columnb_9D[3]], 9, poly_order)
filteredb_A6[columnb_A6[3]] = ss.savgol_filter(b_A6[columnb_A6[3]], 9, poly_order)
filteredb_99[columnb_99[3]] = ss.savgol_filter(b_99[columnb_99[3]], 9, poly_order)
filteredb_80[columnb_80[3]] = ss.savgol_filter(b_80[columnb_80[3]], 9, poly_order)

# In[13] Plotting data before filtering
plt.plot(b_9D[columnb_9D[3]])
plt.plot(b_A6[columnb_A6[3]])
plt.plot(b_99[columnb_99[3]])
plt.plot(b_80[columnb_80[3]])

# In[15] Filtering data for 4500 times
def savgol(df_filtered,poly_order):
    for i in range(1,4501):
        run_filter = ss.savgol_filter(df_filtered, 9, poly_order)
        df_filtered = run_filter
    
    return df_filtered

b_9D_filtered = filteredb_9D[columnb_9D[3]]
b_A6_filtered = filteredb_A6[columnb_A6[3]]
b_99_filtered = filteredb_99[columnb_99[3]]
b_80_filtered = filteredb_80[columnb_80[3]]

b_9D_filtered = savgol(filteredb_9D[columnb_9D[3]],3)
b_A6_filtered = savgol(filteredb_A6[columnb_A6[3]],3)
b_99_filtered = savgol(filteredb_99[columnb_99[3]],3)
b_80_filtered = savgol(filteredb_80[columnb_80[3]],3)

# In[16] Plotting smoothened data
plt.plot(b_9D_filtered)
plt.plot(b_A6_filtered)
plt.plot(b_99_filtered)
plt.plot(b_80_filtered)

# In[17] Showing Final Dataframe with smoothened rssi
b_9D['rssi'] = b_9D_filtered.round(0)
b_A6['rssi'] = b_A6_filtered.round(0)
b_99['rssi'] = b_99_filtered.round(0)
b_80['rssi'] = b_80_filtered.round(0)

# In[19] Converting rssi to distance
# measured_power is the rssi value for 1 meter distance
# N is a constant which depends on environmental factor and ranges from 2-4
# distance = 10**((measured_power-rssi)/(10*N))
N = 3.5
measured_power = -60
b_9D['Distance'] = 10**((measured_power - b_9D['rssi'] )/(10*N))
b_9D['Distance'] = b_9D['Distance'].round(2)

b_A6['Distance'] = 10**((measured_power - b_A6['rssi'] )/(10*N))
b_A6['Distance'] = b_A6['Distance'].round(2)

b_99['Distance'] = 10**((measured_power - b_99['rssi'] )/(10*N))
b_99['Distance'] = b_99['Distance'].round(2)

b_80['Distance'] = 10**((measured_power - b_80['rssi'] )/(10*N))
b_80['Distance'] = b_80['Distance'].round(2)

# In[] Describing Distance
b_9D['Distance'].describe()

# In[]
b_A6['Distance'].describe()

# In[]
b_99['Distance'].describe()

# In[]
b_80['Distance'].describe()

# In[20] Exporting data to Excel
# b_9D.to_excel("D:\\PROJECTS\\Project INPOS\\Filtered_Data\\iter4\\b_9Dnew.xlsx")
# b_A6.to_excel("D:\\PROJECTS\\Project INPOS\\Filtered_Data\\iter4\\b_A6new.xlsx")
# b_99.to_excel("D:\\PROJECTS\\Project INPOS\\Filtered_Data\\iter4\\b_99new.xlsx")
# b_80.to_excel("D:\\PROJECTS\\Project INPOS\\Filtered_Data\\iter4\\b_80new.xlsx")

# In[21] Time Taken
end = time.time()
print(end-start)

#%% 
d1=b_9D['Distance'].mean().round(1)
d2=b_A6['Distance'].mean().round(1)
d3=b_99['Distance'].mean().round(1)
d4=b_80['Distance'].mean().round(1)
print(d1)
print(d2)
print(d3)
print(d4)
# %%
