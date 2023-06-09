# -*- coding: utf-8 -*-
"""EDA_Kaggle.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gXZVlg-aRXeuMSGllTjnqt-RsgoPSd_v

#### data info
"""

import pandas as pd
import numpy as np
from numpy.random import randint 
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import io

from google.colab import files
 
uploaded = files.upload()

data = pd.read_csv(io.BytesIO(uploaded['EaseMyTrip.csv']))
print(data)

## data = pd.read_csv("C:/Users/Khushee Thakker/OneDrive/Desktop/SJSU MSDA/sem 2/DATA270_Sec11_Data Analyt Process/project/EaseMyTrip.csv", delimiter=',', encoding = "utf-8")

data.columns

data.head()

data.tail()

data.shape

data.describe()

data.info()

"""#### Checking missing values"""

data.isnull().sum()

"""#### Check duplicates"""

data.duplicated().sum()

"""#### Droping columns"""

data.drop('Unnamed: 0', axis=1, inplace=True)

flight_data = data

"""#### Univariate Analysis :Exploring each columns"""

import plotly.express as px

"""#### Airline"""

flight_data['airline'].value_counts()

px.histogram(flight_data, x="airline")

"""#### Flights : Flight stores information regarding the plane's flight code. It is a categorical feature."""

flight_data['flight'].value_counts()

"""Top 10 flights"""

flights_Code = flight_data.flight.value_counts().head(10).sort_values(ascending=False)

plt.figure(figsize=(18,6))
flights_Code.plot(kind='bar', color ='purple')
plt.title('Most Frequent Flights',fontsize=15)
plt.xlabel('Flights',fontsize=15)
plt.ylabel('Count',fontsize=15)
plt.show()

"""#### Stops"""

flight_data['stops'].value_counts()

sns.countplot(x=flight_data['stops'] , color = 'lightgreen')

stops = {'one': 1,'zero': 0, 'two_or_more': 2}

flight_data.stops = [stops[item] for item in flight_data.stops]

flight_data['stops'].value_counts()

sns.countplot(x=flight_data['stops'] , color = 'lightgreen')

"""#### Source City and destination_city"""

flight_data['source_city'].value_counts()

src_city = {'Mumbai': 'BOM','Delhi': 'DEL', 'Bangalore': 'BLR', 'Kolkata': 'CCU', 'Hyderabad': 'HYD', 'Chennai': 'MAA'}
flight_data.source_city = [src_city[item] for item in flight_data.source_city]

flight_data['source_city'].value_counts()

flight_data['destination_city'].value_counts()

dest_city = {'Mumbai': 'BOM','Delhi': 'DEL', 'Bangalore': 'BLR', 'Kolkata': 'CCU', 'Hyderabad': 'HYD', 'Chennai': 'MAA'}
flight_data.destination_city = [dest_city[item] for item in flight_data.destination_city]

flight_data['destination_city'].value_counts()

import matplotlib.pyplot as plt

sns.countplot(x=flight_data["destination_city"] , color = 'lightblue')

sns.countplot(x=flight_data["source_city"] , color = 'lightpink')

"""#### departure_time and arrival_time"""

flight_data['departure_time'].value_counts()

## dept_time = {'Morning': '10:00','Early_Morning': '08:00', 'Evening': '18:00', 'Night': '22:00','Afternoon': '13:00', 'Late_Night': '02:00'}

## flight_data.departure_time = [dept_time[item] for item in flight_data.departure_time]

##data['departure_time'].value_counts()

flight_data['arrival_time'].value_counts()

"""#### Class"""

flight_data['class'].value_counts()

flight_data["class"].value_counts().plot(kind='pie', autopct='%1.1f%%')

flight_data.columns

"""#### Duration"""

flight_data['duration'].value_counts()

from numpy.core.fromnumeric import sort
sort(flight_data['duration'])

import math
flight_data['duration'] = (flight_data['duration'] * 60).astype('int')

flight_data['duration']

flight_data

"""#### Checking outliers for columns"""

plt.hist(flight_data['price'])

"""duration"""

px.box(data, x="duration", orientation="h")

"""#### Data visualizations for EDA"""

from sklearn.preprocessing import LabelEncoder
labelencoder=LabelEncoder()

flight_data.head()

#data['airline']=labelencoder.fit_transform(data['airline'])
#data['flight']=labelencoder.fit_transform(data['flight'])
#data['source_city']=labelencoder.fit_transform(data['source_city'])
#data['departure_time']=labelencoder.fit_transform(data['departure_time'])
#data['arrival_time']=labelencoder.fit_transform(data['arrival_time'])
#data['destination_city']=labelencoder.fit_transform(data['destination_city'])
#data['class']=labelencoder.fit_transform(data['class'])

flight_Count = flight_data.groupby(['flight','airline'],as_index=False).count()

plt.figure(figsize=(8,5))
sns.countplot(flight_Count.airline,palette='hls')
plt.title('Flights Count of Different Airlines',fontsize=15)
plt.xlabel('Airline',fontsize=15)
plt.ylabel('Count',fontsize=15)
plt.show()

"""Most Frequent takeoff city"""

plt.figure(figsize=(18,6))
sns.countplot(flight_data['source_city'],palette='hls')
plt.title('Most Frequent takeoff City',fontsize=15)
plt.xlabel('source_city',fontsize=15)
plt.ylabel('Count',fontsize=15)
plt.show()

"""Time of Departure"""

plt.figure(figsize=(18,6))
sns.countplot(flight_data['departure_time'],palette='Paired')
plt.title('Time of Departure',fontsize=15)
plt.xlabel('Departure Time',fontsize=15)
plt.ylabel('Count',fontsize=15)
plt.show()

#### Time of Arrival

plt.figure(figsize=(18,6))
sns.countplot(flight_data['arrival_time'],palette='Paired')
plt.title('Arrival Time of Flights',fontsize=15)
plt.xlabel('Arrival Time',fontsize=15)
plt.ylabel('Count',fontsize=15)
plt.show()

#### How does the ticket price vary between Economy and Business class?

class_Ticket_Price = flight_data.groupby(['class'])['price'].mean()

print(class_Ticket_Price)

plt.figure(figsize=(12,5))
class_Ticket_Price.plot(kind='bar')
plt.title('Average Ticket price of Business and Economy Class',fontsize=15)
plt.xlabel('Class',fontsize=15)
plt.xticks(rotation=0)
plt.ylabel('Count',fontsize=15)
plt.show()

flight_data.groupby(['airline'])['class'].count()

####  How the price changes with change in Source and Destination?

flight_data.groupby(['airline','source_city','destination_city'],as_index=False)['price'].mean()

plt.figure(figsize=(24,10))
plt.subplot(1,2,1)
sns.violinplot(x='source_city',y='price',data=data)
plt.title('Source City Vs Ticket Price',fontsize=20)
plt.xlabel('Source City',fontsize=15)
plt.ylabel('Price',fontsize=15)

plt.subplot(1,2,2)
sns.violinplot(x='destination_city',y='price',data=data,palette='hls')
plt.title('Destination City Vs Ticket Price',fontsize=20)
plt.xlabel('Destination City',fontsize=15)
plt.ylabel('Price',fontsize=15)
plt.show()

"""#### Bivariate"""

px.scatter(flight_data, x="price", y="stops")

px.scatter(flight_data, x="price", y="duration")

sns.boxplot(data=flight_data, x="stops", y="price")

#sns.boxplot(y = "price", x = "Source", data = df.sort_values("Price", ascending = False))
#plt.show()

#sns.kdeplot(data=flight_data, x="price", hue="class")

"""#### Multivariate

price varies with the flight duration based on class
"""

plt.figure(figsize = (16, 8))
sns.lineplot(data = flight_data, x = 'duration', y= 'price', hue = 'class')
plt.title('Ticket Price Versus Flight Duration Based on Class')
plt.show()

"""price affected on the days left for departure for each airline"""

plt.figure(figsize = (16, 8))
sns.lineplot(data = flight_data, x = 'days_left', y= 'price', hue = 'airline')
plt.title('Ticket Price Versus Days Left')
plt.show()

"""#### New stop correction"""

flight_data = flight_data.rename(columns={"airline": "flight_one"})

flight_data["flight_two"] = 'None'
flight_data["flight_three"] = 'None'

flight_data

len(flight_data[(flight_data['stops']==1)&(flight_data['flight_two']=='None')])

flight_data['flight_two']=np.where((flight_data['stops']==1), flight_data['flight_one'],flight_data['flight_two'])

len(flight_data[(flight_data['stops']=='1')&(flight_data['flight_two']=='None')])

flight_data[(flight_data['stops'])==1]

## Checking the number of rows where stop =2 and there are no flight data about extra flights
len(flight_data[(flight_data['stops']==2)&(flight_data['flight_two'] == 'None')])

flight_data['flight_two']=np.where((flight_data['stops']==2), flight_data['flight_one'],flight_data['flight_two'])

flight_data['flight_three']=np.where((flight_data['stops']==2), flight_data['flight_one'],flight_data['flight_three'])

flight_data[(flight_data['stops'])==2]

flight_data

"""#### drop"""

flight_data

flight_data = flight_data.drop('flight', axis=1)

"""#### Download files"""

flight_data.to_csv('data_kaggle.csv')

files.download("data_kaggle.csv")

"""#### Merging"""

from google.colab import files
 
uploaded = files.upload()

data_kayak = pd.read_csv(io.BytesIO(uploaded['cleaned_kayak.csv']))
print(data_kayak)

data_kayak.drop('Unnamed: 0', axis=1, inplace=True)

data_kayak.head()

data_kayak = data_kayak.rename(columns={"origin": "source_city", "destination": "destination_city", "stop" : "stops","deptime" : "departure_time", "arrtime" : "arrival_time", "duration_mins" : "duration"})

##flight_data.append(df2, ignore_index = True)

frames = [flight_data, data_kayak]

merge_flightdata = pd.concat(frames)

merge_flightdata.to_csv('merge_flightdata.csv')
files.download("merge_flightdata.csv")

merge_flightdata

"""#### EDA merge data"""

merge_flightdata.duplicated().sum()



merge_flightdata.shape

merge_flightdata.info()

merge_flightdata

merge_flightdata['flight_two'].value_counts()

merge_flightdata['flight_three'].value_counts()

merge_flightdata['flight_one'].value_counts()

merge_flightdata['source_city'].value_counts()

merge_flightdata['destination_city'].value_counts()

merge_flightdata['arrival_time'].value_counts()

merge_flightdata['departure_time'].value_counts()

merge_flightdata['stops'].value_counts()

merge_flightdata['class'].value_counts()

plt.hist(merge_flightdata['price'])

plt.hist(merge_flightdata['duration'])

sns.countplot(x=merge_flightdata['stops'])

