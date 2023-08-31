
# coding: utf-

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import os
from OnlineModeDataStream import OnlineModeDataStream

ds = OnlineModeDataStream()
#importing dataset
dataset = pd.read_csv(os.path.join(ds.getInputDirName(),'RK_12-13.csv'))
df = pd.DataFrame(dataset)



#populating zero greendrive values 
df['greenDriveValue'].fillna(value=0, inplace = True)
df['greenDriveType'].fillna(value=0, inplace = True)

#adding ha, hb,hc columns
df['HA']= df['greenDriveValue']*0
df['HB']= df['greenDriveValue']*0
df['HC']= df['greenDriveValue']*0

#populating ha,hb,hc
for index, row in df.iterrows():
    if df.loc[index,'greenDriveType'] == 3:
        df.loc[index,'HC'] = df.loc[index,'greenDriveValue']
    if df.loc[index,'greenDriveType'] == 2:
        df.loc[index,'HB'] = df.loc[index,'greenDriveValue']
    if df.loc[index,'greenDriveType'] == 1:
        df.loc[index,'HA'] = df.loc[index,'greenDriveValue']

#populating os
for index, row in df.iterrows():
    if df.loc[index,'speed'] >= 35:
        df.loc[index,'OS'] = (df.loc[index,'speed']*2 - 70)*50/35
    else:
        df.loc[index,'OS'] = 0

#converting time to minutes
import datetime

for index, row in df.iterrows():
    #if df.loc[index,'speed'] >= 50:
     df.loc[index,'Time'] =datetime.datetime.fromtimestamp(df.loc[index, 'timestamp']).strftime('%H:%M:%S')

df['Time'].str.split(':').head()
df['Time']= df['Time'].str.split(':').apply(lambda x: (int(x[0]) * 3600 + int(x[1])*60 + int(x[2]))/60)

#getting acceleration
for index, row in df.iterrows():
    df.loc[index,'acc'] = 0
for index, row in df.iterrows():
     if(df.iloc[index-1, 51] - df.iloc[index, 51]) != 0:
         df.iloc[index,52] =(int)(df.iloc[index-1, 2] - df.iloc[index, 2])/(df.iloc[index-1, 51] - df.iloc[index, 51])

# v*a
for index, row in df.iterrows():
    df.loc[index,'v*a']= df.loc[index,'acc']*df.loc[index,'speed']


#scaling all parameters
df['HA']= (df['HA']-np.mean(df['HA']))/np.std(df['HA'])
df['HB']= (df['HB']-np.mean(df['HB']))/np.std(df['HB'])
df['HC']= (df['HC']-np.mean(df['HC']))/np.std(df['HC'])
df['OS']= (df['OS']-np.mean(df['OS']))/np.std(df['OS'])
df['v*a']= (df['v*a']-np.mean(df['v*a']))/np.std(df['v*a'])


#importing imp columns in a fresh df
df1 = df[['v*a','HA','HB','HC','OS']]


#determine number of clusters
from sklearn.cluster import KMeans
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters = i, init = 'k-means++')
    kmeans.fit(df1)
    wcss.append(kmeans.inertia_)
# plt.plot(range(1,11),wcss)
# plt.show()


from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=5)


kmeans.fit(df1[['HA','HB','HC','OS','v*a']])


a = kmeans.labels_


ans = pd.Series(data = a)


df1['Behavior'] = ans
for i in range(10):
    speed = ds.retrieveData("SPEED")
    if speed != None:
        ds.sendDataOut(speed)
    lat_deg = ds.retrieveData("LAT_DEG")
    lat_dec = ds.retrieveData("LAT_DEC")
    if lat_deg != None and lat_dec != None:
        latitude = lat_deg + lat_dec
        ds.sendDataOut(latitude)
    long_deg = ds.retrieveData("LONG_DEG")
    long_dec = ds.retrieveData("LONG_DEC")
    if long_deg != None and long_dec != None:
        longitude = long_deg + long_dec
        ds.sendDataOut(longitude)

# for index, row in df1.iterrows():
#     # ds.sendDataOut(row['Behavior'])
#     #send some GPS coordinates >:)
#     if index%10 == 0:
#         for i in range(10):
#             speed = ds.retrieveData("SPEED")
#             if speed != None:
#                 ds.sendDataOut(speed)
#             lat_deg = ds.retrieveData("LAT_DEG")
#             lat_dec = ds.retrieveData("LAT_DEC")
#             if lat_deg != None and lat_dec != None:
#                 latitude = lat_deg + lat_dec
#                 ds.sendDataOut(latitude)
#             long_deg = ds.retrieveData("LONG_DEG")
#             long_dec = ds.retrieveData("LONG_DEC")
#             if long_deg != None and long_dec != None:
#                 longitude = long_deg + long_dec
#                 ds.sendDataOut(longitude)



