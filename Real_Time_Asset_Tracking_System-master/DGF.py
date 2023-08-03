# In[1]: Importing Libraries
from IPython import get_ipython
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as ss
import numpy as np
import time
from scipy.ndimage.filters import gaussian_filter

# In[2]: Reading Data into Dataframe 
df = pd.read_excel(r"D:\PROJECTS\Project INPOS\Dump_Data\Trial on 29-3\Trial 1.xlsx")
df = df.drop(df.columns[[1,2,3,7,8]],axis=1)
# %%
df.info()
# %%
df.columns = ['SNO','Time','Beacon_Mac','rssi']
# %%
df['Time'] = pd.to_datetime(df['Time'])
df['seconds'] = (df['Time'].dt.hour)* 3600 + (df['Time'].dt.minute)*60 + (df['Time'].dt.second) 
# %%
b_9D = df[df['Beacon_Mac'] == "C645C401019D"].copy()
b_A6 = df[df['Beacon_Mac'] == "C645C40101A6"].copy()
b_99 = df[df['Beacon_Mac'] == "C645C4010199"].copy()
b_80 = df[df['Beacon_Mac'] == "C645C4010180"].copy()

print(b_9D)
print(b_A6)
print(b_99)
print(b_80)


# %%
columnb_9D = list(b_9D.columns)
columnb_A6 = list(b_A6.columns)
columnb_99 = list(b_99.columns)
columnb_80 = list(b_80.columns)
# %%
filteredb_9D = {}
filteredb_A6 = {}
filteredb_99 = {}
filteredb_80 = {}
#gaussian_filter(b_9D[columnb_9D[3]], sigma=7)
filteredb_9D[columnb_9D[3]] = gaussian_filter(b_9D[columnb_9D[3]], sigma=7)
filteredb_A6[columnb_A6[3]] = gaussian_filter(b_A6[columnb_A6[3]], sigma=7)
filteredb_99[columnb_99[3]] = gaussian_filter(b_99[columnb_99[3]], sigma=7)
filteredb_80[columnb_80[3]] = gaussian_filter(b_80[columnb_80[3]], sigma=7)
# %%
plt.plot(b_9D[columnb_9D[3]])
plt.plot(b_A6[columnb_A6[3]])
plt.plot(b_99[columnb_99[3]])
plt.plot(b_80[columnb_80[3]])
# %%
def savgol(df_filtered,sigma):
    for i in range(1,2):
        run_filter = gaussian_filter(df_filtered, sigma)
        df_filtered = run_filter
    
    return df_filtered
b_9D_filtered = savgol(filteredb_9D[columnb_9D[3]],7)
b_A6_filtered = savgol(filteredb_A6[columnb_A6[3]],7)
b_99_filtered = savgol(filteredb_99[columnb_99[3]],7)
b_80_filtered = savgol(filteredb_80[columnb_80[3]],7)
# %%
plt.plot(b_9D_filtered)
plt.plot(b_A6_filtered)
plt.plot(b_99_filtered)
plt.plot(b_80_filtered)
# %%
b_9D['rssi'] = b_9D_filtered.round(0)
b_A6['rssi'] = b_A6_filtered.round(0)
b_99['rssi'] = b_99_filtered.round(0)
b_80['rssi'] = b_80_filtered.round(0)
# %%
N = 2.5
measured_power = -65
def dist(b):
    b['Distance'] = 10**((measured_power - b['rssi'] )/(10*N))
    b['Distance'] = b['Distance'].round(2)

dist(b_9D)
dist(b_A6)
dist(b_99)
dist(b_80)
# %%
print(b_9D['Distance'].mean())
print(b_A6['Distance'].mean())
print(b_99['Distance'].mean())
print(b_80['Distance'].mean())
# %%
