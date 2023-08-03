# In[1]: Importing Libraries
from IPython import get_ipython
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as ss
import time

# In[2]: Reading Data into Dataframe 
df = pd.read_excel("D:\IPS\Real_Time_Asset_Tracking_System\Dump_Data\Thursday\Report_1677132817130.xlsx")
df = df.drop(df.columns[[1,2,3,7,8]],axis=1)
# In[4] Naming The Columns
df.columns = ['SNO','Time','Beacon_Mac','rssi']

# In[5] Getting The Seconds from the timestamp
df['Time'] = pd.to_datetime(df['Time'])
df['seconds'] = (df['Time'].dt.hour)* 3600 + (df['Time'].dt.minute)*60 + (df['Time'].dt.second) 
rsi_avg=df['rssi'].mean()
print(rsi_avg)
# %%
b1 = df[df['Beacon_Mac'] == "C645C401019D"].copy()
b2 = df[df['Beacon_Mac'] == "C645C40101A6"].copy()
b3 = df[df['Beacon_Mac'] == "C645C4010199"].copy()
b4 = df[df['Beacon_Mac'] == "C645C4010180"].copy()
# %%
poly_order = 3

# In[8] Making the columns of the Dataframe into a list variable 
columnb1 = list(b1.columns)
columnb2 = list(b2.columns)
columnb3 = list(b3.columns)
columnb4 = list(b4.columns)
# %%
filteredb1 = {}
filteredb2 = {}
filteredb3 = {}
filteredb4 = {}
filteredb1[columnb1[3]] = ss.savgol_filter(b1[columnb1[3]], 9, poly_order)
filteredb2[columnb2[3]] = ss.savgol_filter(b2[columnb2[3]], 9, poly_order)
filteredb3[columnb3[3]] = ss.savgol_filter(b3[columnb3[3]], 9, poly_order)
filteredb4[columnb4[3]] = ss.savgol_filter(b4[columnb4[3]], 9, poly_order)
# %%
plt.plot(b1[columnb1[3]])
plt.plot(b2[columnb2[3]])
plt.plot(b3[columnb3[3]])
plt.plot(b4[columnb4[3]])
# %%
def savgol(df_filtered,poly_order):
    for i in range(1,4501):
        run_filter = ss.savgol_filter(df_filtered, 9, poly_order)
        df_filtered = run_filter
    
    return df_filtered
b1_filtered = savgol(filteredb1[columnb1[3]],3)
b2_filtered = savgol(filteredb2[columnb1[3]],3)
b3_filtered = savgol(filteredb3[columnb3[3]],3)
b4_filtered = savgol(filteredb4[columnb1[3]],3)
# %%
plt.plot(b1_filtered)
plt.plot(b2_filtered)
plt.plot(b3_filtered)
plt.plot(b4_filtered)
# %%
b1['rssi'] = b1_filtered.round(0)
b2['rssi'] = b2_filtered.round(0)
b3['rssi'] = b3_filtered.round(0)
b4['rssi'] = b4_filtered.round(0)
# %%#######################
N = 2
measured_power = -83
'''[]
measured_power.append(b1['rssi'].mean().round(0))
measured_power.append(b2['rssi'].mean().round(0))
measured_power.append(b3['rssi'].mean().round(0))
measured_power.append(b4['rssi'].mean().round(0))'''
#print(measured_power)

def dist(b):
    b['Distance'] = 10**((measured_power - b['rssi'] )/(10*N))
    b['Distance'] = b['Distance'].round(2)

dist(b1)
dist(b2)
dist(b3)
dist(b4)
# %%
'''b1.to_excel("D:\\PROJECTS\\Project INPOS\\Filtered_Data\\iter5\\B1_103_4.xlsx")
b2.to_excel("D:\\PROJECTS\\Project INPOS\\Filtered_Data\\iter5\\B2_103_4.xlsx")
b3.to_excel("D:\\PROJECTS\\Project INPOS\\Filtered_Data\\iter5\\B3_103_4.xlsx")
b4.to_excel("D:\\PROJECTS\\Project INPOS\\Filtered_Data\\iter5\\B4_103_4.xlsx")'''
# %%
d1=b1['Distance'].mean().round(1)
d2=b2['Distance'].mean().round(1)
d3=b3['Distance'].mean().round(1)
d4=b4['Distance'].mean().round(1)
print(d1)
print(d2)
print(d3)
print(d4) #we will consider it as moving beacon..
#now we will try to do positioning of moving beacon using 2 gateways
# Enter distance of those 3 beacons from gateways g1 and g2 then give position details of 3 becons lets
# say its coordinates after that we will calculate g1 and g2 coordinates after that for beacon 4 we will 
# calculate its position with respect to g1 and g2 as there is no relation between other 3 beacons 
# and 4th one. 
# %%
print(b4)
# %%
