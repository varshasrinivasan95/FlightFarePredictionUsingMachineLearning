# -*- coding: utf-8 -*-
"""mergeEDA+Cleaning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cMi9JNC-oXmc31hSWCtU0ScDavPhtmyZ

# Reading Data
"""

from google.colab import files
 
uploaded = files.upload()

print (uploaded['merge_flightdata.csv'][:200].decode('utf-8') + '...')

"""# Import Libraries"""

import pandas as pd
import numpy as np
from numpy.random import randint 
import seaborn as sns
import matplotlib.pyplot as plt
import io
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

"""# Data Exploration"""

merge_flightdata = pd.read_csv(io.BytesIO(uploaded['merge_flightdata.csv']))

merge_flightdata

len(merge_flightdata)

merge_flightdata.shape

merge_flightdata.info()

merge_flightdata.head()

merge_flightdata.tail()

merge_flightdata.nunique()

merge_flightdata.describe(include='all')

"""# Dropping Inappropriate Column"""

merge_flightdata=merge_flightdata.drop(columns=['Unnamed: 0'])

merge_flightdata.head(5)

"""# Missing Values Treatment"""

merge_flightdata.isnull().sum()

"""**Observations**
- We notice null values in flight_two column
- Populating 'None' values for the null places of flight_two column
"""

merge_flightdata["flight_two"]=np.where((merge_flightdata['flight_two'].isnull()),'None',merge_flightdata["flight_two"])

merge_flightdata.isnull().sum()

"""# Checking Duplicate Entries"""

merge_flightdata.duplicated().sum()

## Dropping the duplicate values
merge_flightdata=merge_flightdata.drop_duplicates()

merge_flightdata.duplicated().sum()

"""# Univariate Analysis

#####**Flight_one Column**
"""

merge_flightdata['flight_one'].value_counts()

### Changing the inapproriate values of Air_India,Indigo,Go first
merge_flightdata['flight_one'] =merge_flightdata['flight_one'].str.replace('Air_India', 'Air India')
merge_flightdata['flight_one'] =merge_flightdata['flight_one'].str.replace('GO_FIRST', 'Go First')
merge_flightdata['flight_one'] =merge_flightdata['flight_one'].str.replace('GoFirst', 'Go First')
merge_flightdata['flight_one'] =merge_flightdata['flight_one'].str.replace('Indigo', 'IndiGo')

merge_flightdata['flight_one'].value_counts()

"""#####**Flight_two Column**"""

merge_flightdata['flight_two'].value_counts()

##removing white space from starting of the column
merge_flightdata['flight_two']=merge_flightdata['flight_two'].str.strip()

merge_flightdata['flight_two'].value_counts()

"""##### **Flight_three Column**"""

merge_flightdata['flight_three'].value_counts()

##removing white space from starting of the column
merge_flightdata['flight_three']=merge_flightdata['flight_three'].str.strip()

merge_flightdata['flight_three'].value_counts()

"""##### **Stops Column**"""

merge_flightdata['stops'].value_counts()

sns.countplot(x=merge_flightdata['stops'])

"""####**Class Column** """

merge_flightdata['class'].value_counts()

sns.countplot(x=merge_flightdata['class'],color='lightgreen')

"""#### **Price Column**"""

merge_flightdata['price'].value_counts()

plt.hist(merge_flightdata['price'], color = "lightgreen")
plt.xlabel('Price ',fontsize=15)

"""#### **Departure_time Column**"""

merge_flightdata['departure_time'].value_counts()

plt.figure(figsize =(10,6))
plt.title('Percentage breakdown of flight departure time', fontsize=15, color='Green')
merge_flightdata["departure_time"].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.ylabel('')
plt.show()

"""####**Arrival_time Column**"""

merge_flightdata['arrival_time'].value_counts()

plt.figure(figsize =(10,6))
plt.title('Percentage breakdown of flight arrival time', fontsize=15, color='Green')
merge_flightdata["arrival_time"].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.ylabel('')
plt.show()

"""# **Duration**"""

plt.hist(merge_flightdata['duration'], color = "skyblue")
plt.xlabel('Duration ',fontsize=15)

"""#### **Source_city Column**"""

merge_flightdata['source_city'].value_counts()

sns.countplot(x=merge_flightdata['source_city'])

"""#### **Destination City Column**"""

merge_flightdata['destination_city'].value_counts()

sns.countplot(x=merge_flightdata['destination_city'])

"""# Analysis"""

plt.figure(figsize=(10,10))
sns.heatmap(merge_flightdata.corr(),  annot=True)

"""plt.stackplot(df.Class, df.sec_A, df.sec_B, df.sec_C,
              labels=['Sec A', 'Sec B', 'Sec C'],
              colors=color_map)
"""

plt.figure(figsize=(15,10))
sns.scatterplot(x = 'price',y = 'duration',hue = 'class',data=merge_flightdata)

"""pair plot"""

sns.pairplot(merge_flightdata)
plt.show()

merge_flightdata

"""# Training Model

##### Encoding - converting categorical to numeric data
"""

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
for col in merge_flightdata.columns:
    if merge_flightdata[col].dtype == 'object':
        merge_flightdata[col] = le.fit_transform(merge_flightdata[col])

merge_flightdata

sns.pairplot(merge_flightdata)
plt.show()

plt.figure(figsize=(10,10))
sns.heatmap(merge_flightdata.corr(),  annot=True)

"""##### Segregate target and desriptive feature"""

x = merge_flightdata.drop(['price'], axis = 1)
y = merge_flightdata['price']

x

y

"""##### Split into train and test"""

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.30, random_state = 42)
x_train.shape, y_train.shape, x_test.shape, y_test.shape

x_train.head()

x_test.head()

"""##### Performing Normalization (Range [0,1])"""

from sklearn.preprocessing import MinMaxScaler
minmaxscale = MinMaxScaler(feature_range = (0, 1))
x_train = minmaxscale.fit_transform(x_train)
x_test = minmaxscale.fit_transform(x_test)
x_train = pd.DataFrame(x_train)
x_test = pd.DataFrame(x_test)

x_train

x_test

"""##### Building linear regression model"""

from sklearn.linear_model import LinearRegression

linear_reg = LinearRegression()
linear_reg.fit(x_train, y_train)
y_pred = linear_reg.predict(x_test)

from sklearn import metrics

print('Mean Absolute Error (MAE):', round(metrics.mean_absolute_error(y_test, y_pred),3))  
print('Mean Squared Error (MSE):', round(metrics.mean_squared_error(y_test, y_pred),3))  
print('Root Mean Squared Error (RMSE):', round(np.sqrt(metrics.mean_squared_error(y_test, y_pred)),3))
print('R2_score:', round(metrics.r2_score(y_test, y_pred),6))

"""##### KNN"""

from sklearn.neighbors import KNeighborsRegressor

KNN_reg = KNeighborsRegressor()
KNN_reg.fit(x_train, y_train)
knn_y_pred = KNN_reg.predict(x_test)

print('Mean Absolute Error (MAE):', round(metrics.mean_absolute_error(y_test, knn_y_pred),3))  
print('Mean Squared Error (MSE):', round(metrics.mean_squared_error(y_test, knn_y_pred),3))  
print('Root Mean Squared Error (RMSE):', round(np.sqrt(metrics.mean_squared_error(y_test, knn_y_pred)),3))
print('R2_score:', round(metrics.r2_score(y_test, knn_y_pred),6))

"""#####  Decision Tree

"""

from sklearn.tree import DecisionTreeRegressor

dec_reg = DecisionTreeRegressor()
dec_reg.fit(x_train, y_train)
dec_y_pred = dec_reg.predict(x_test)

print('Mean Absolute Error (MAE):', round(metrics.mean_absolute_error(y_test, dec_y_pred),3))  
print('Mean Squared Error (MSE):', round(metrics.mean_squared_error(y_test, dec_y_pred),3))  
print('Root Mean Squared Error (RMSE):', round(np.sqrt(metrics.mean_squared_error(y_test, dec_y_pred)),3))
print('R2_score:', round(metrics.r2_score(y_test, dec_y_pred),6))

"""##### Data Regularization

###### Lasso
"""

from sklearn.linear_model import Ridge, Lasso

lm = Lasso(alpha = 0.1)
lm.fit(x_train, y_train)
lm_y_pred = lm.predict(x_test)

print('Mean Absolute Error (MAE):', round(metrics.mean_absolute_error(y_test, lm_y_pred),3))  
print('Mean Squared Error (MSE):', round(metrics.mean_squared_error(y_test, lm_y_pred),3))  
print('Root Mean Squared Error (RMSE):', round(np.sqrt(metrics.mean_squared_error(y_test, lm_y_pred)),3))
print('R2_score:', round(metrics.r2_score(y_test, lm_y_pred),6))

"""###### Ridge"""

rm = Ridge()
rm.fit(x_train, y_train)
rm_y_pred = rm.predict(x_test)

print('Mean Absolute Error (MAE):', round(metrics.mean_absolute_error(y_test, rm_y_pred),3))  
print('Mean Squared Error (MSE):', round(metrics.mean_squared_error(y_test, rm_y_pred),3))  
print('Root Mean Squared Error (RMSE):', round(np.sqrt(metrics.mean_squared_error(y_test, rm_y_pred)),3))
print('R2_score:', round(metrics.r2_score(y_test, rm_y_pred),6))