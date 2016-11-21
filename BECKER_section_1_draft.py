#########################################################################
## Section 1                                                           ##
#########################################################################
from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os
import csv
import xlrd
import time
import matplotlib.pyplot as plt
import pytz
import statsmodels.api as sm #package developed to do stats analyses
from datetime import datetime, timedelta
from dateutil import parser

# PART A ----------------------------------------------------------------------

#1) Import and stack gas consumption files. 
main_dir = "C:/Users/J/Desktop/data/"
root = main_dir + "final/"
sect1 = root + "section_1/"
sect2 = root + "section_2/"
paths = [os.path.join(sect1, v) for v in os.listdir(sect1) if v.startswith("gas_long_redux_")]

## Import and stack data
df = pd.concat([pd.read_csv(v) for v in paths], ignore_index=True)

#2) Clean the data. 
## 2.1) Replace missing and negative values with zero. 
df = df.fillna(0)
df['kwh'][df['kwh'] < 0] = 0 
df[:20]

## 2.2) Drop obs with duplicate IDs and dates, ignoring consumption. 
df = df.drop_duplicates(['ID', 'date_cer'], take_last = True)


print "\n\n\n"
print df.shape
print df.kwh.mean()

# PART B ----------------------------------------------------------------------
# 1) Import the allocation and time series correction data 
alloc = pd.read_csv(sect1 + "residential_allocations.csv", usecols=[0,1])
time_corr = pd.read_csv(sect1 + "time_correction.csv")
alloc.head()
time_corr.head()
df.head()

# 2) Merge both data sets to the clean DataFrame, df
 ## Merge allocation with consumption data
df1 = pd.merge(alloc, df, on = 'ID')
df1['hour_cer'] = (df1.date_cer % 100)
df1['day_cer'] = (df1.date_cer - df1['hour_cer'])/100
df1.head()

 ## Merge consumption/allocation dataframe with time series correction; go back to calling it df
df = pd.merge(df1, time_corr, on=['hour_cer', 'day_cer'])
df.head()

print "\n\n\n"
print df[df.ID == 1021].head(20) 

# PART C ----------------------------------------------------------------------
# 1) Aggregate household consumption by month 
monthgroup = df.groupby(['ID', 'allocation', 'year', 'month'])
df_monthly = monthgroup['kwh'].sum().reset_index()
df_monthly.head()

# 2) Pivot the monthly data from long to wide. 
 ##First, create variables, then pivot.
df_monthly['kwh_month'] = 'kwh_' + df_monthly.month.apply(str)
df_piv = df_monthly.pivot('ID', 'kwh_month', 'kwh')
df_piv.reset_index(inplace=True)
df_piv.columns.name = None
df_piv.head()

print "\n\n\n"
print df_piv.shape
print df_piv.head()

# PART D ----------------------------------------------------------------------
# 1) Aggregate household consumption by month, using "ym" variable.
monthgroup = df.groupby(['ID', 'allocation', 'ym'])
df_monthly = monthgroup['kwh'].sum().reset_index()
df_monthly.head()
#df_monthly will show me each household's total monthly consumption


# 2) Get average monthly consumption by treatment assignment.
group_treatmonth = df_monthly.groupby(['allocation', 'ym'])
avg_monthlycons_bytrt = group_treatmonth['kwh'].mean()
avg_monthlycons_bytrt[:20]
#avg_monthlycons_bytrt will show me average monthly consumption by treatment group

# 3 Plot average monthly consumption by treatment group. 
fig1 = avg_monthlycons_bytrt.unstack().transpose().plot()
fig1.set_title('Average Monthly Consumption by Treatment Group')

