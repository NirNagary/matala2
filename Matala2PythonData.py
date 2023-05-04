# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 17:12:03 2023

@author: annak
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import datetime as dt
import re
from datetime import timedelta
#Q1

data = pd.read_csv("matala2_cosmetics_2019-Nov.csv", low_memory=False)#


data['time'] = data['event_time'].str.split().str[1]
data['date'] = data['event_time'].str.split().str[0]
data['event_time'] = pd.to_datetime(data['date'] + ' ' + data['time'], format='%Y-%m-%d %H:%M:%S')

data['duration_to_next_event'] = data.groupby('user_session')['event_time'].shift(-1) - data['event_time']
data['duration_to_next_event'] = data['duration_to_next_event'].fillna(pd.Timedelta(seconds=0))




#Q2


data['time_diff']=data.groupby(['user_id'])['event_time'].diff()

data['funnel_number'] = data.groupby(['user_id'])['time_diff'].apply(lambda x: (x >= timedelta(days=5)).cumsum()) +1
#data['funnel_number'] = (data.groupby(['user_id'])['funnel_number'].apply(lambda x: x.cummax()))


#Q3
data['index_in_funnel'] = data.groupby(['user_id', 'funnel_number'])['user_session'].transform(lambda x: pd.CategoricalIndex(x).codes+1)

#Q4
data['price'] = data['price'].apply(lambda x :float(re.findall(r'\d+\.\d+',x)[0]))

#Q5
import seaborn as sns

# Create the count plot
sns.countplot(x="event_type", data=data)

# Add labels and title
plt.xlabel("Event types")
plt.ylabel("Count")
plt.title("Number of event types")

# Show the plot
plt.show()

#Q6
data6= data.copy()
data6['total_events']= data.groupby('user_session')['event_type'].transform('count')

# Group the data by 'user_session'
grouped = data6.groupby('user_session')

# Calculate the duration of each session
temp = grouped['event_time'].max() - grouped['event_time'].min()
# data6
# data6[data6['user_id']== 566307474]

data6 = pd.merge(data6, temp, on='user_session', how='right')

data6 = data6.rename(columns={'event_time_y': 'session_duration'})

patient_level_df = data6.groupby(['user_session','event_type']).agg(
{
    'product_id': lambda x: list(set(x))
}).reset_index()

# pivot the data by user_session and event_type
pivot_df = patient_level_df.pivot_table(index='user_session', columns='event_type', values='product_id', aggfunc='first')

# reset the index to make the user_session a regular column
result = pivot_df.reset_index()
result

data6.drop_duplicates(subset='user_session', inplace=True)
data6 = pd.merge(data6, result, on='user_session', how='right')

data6.columns=['event_time', 'event_type', 'product_id', 'category_id',
       'category_code', 'brand', 'price', 'user_id', 'user_session', 'funnel',
       'bigger_than5', 'funnel_number', 'total_events', 'session_duration',
       'list_of_added_to_cart', 'list_of_purchased', 'remove_from_cart', 'list_of_viewed']
data6 = pd.merge(data6, data, on='user_session', how='right')
session_data= data6.drop(['event_time', 'event_type', 'product_id', 'category_id',
       'category_code', 'brand', 'price', 'funnel', 'bigger_than5', 'remove_from_cart'], axis=1)

session_data.dropna(subset=['user_id'], inplace=True)






pd.set_option('display.max_columns', None)

                                        


print(data.head(5))

