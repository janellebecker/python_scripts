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

main_dir = "C:/Users/J/Desktop/data/"
root = main_dir + "grouptask4/"

#--------------------------------------------------------------------------
# Section I
# -------------------------------------------------------------------------

# CHANGE WORKING DIRECTORY ----------------
os.chdir(root)
from logit_functions import *

# IMPORT DATA -----------------------------
df = pd.read_csv(root + "task_4_kwh_w_dummies_wide.csv")
df = df.dropna(axis=0, how='any')

# GET TARIFFS ----------------------------
df.head()
tariffs = [v for v in df['tariff'].unique() if v != 'E']
stim = [v for v in df['stimulus'].unique() if v != 'E']
tariffs.sort()
stim.sort()

# RUN LOGIT MODELS TO CHECK FOR BALANCE ------------------------
df_drop = [v for v in df.columns if v.startswith("kwh_2010")]
df_pretrial = df.drop(df_drop, axis=1)
df_pretrial.head()


for i in tariffs:
    for j in stim:
        logit_reults, df_logit = do_logit(df_pretrial, i, j, add_D=None, mc=False)

# COMPARISON OF MEANS WITH T-TESTS
group = df_logit.groupby('tariff')
df_mean = group.mean().transpose()
df_std = group.std().transpose()
df_N = group.count().transpose().mean()

top = df_mean['C'] - df_mean['E']
bottom = np.sqrt((df_std['C']**2/df_N['C']) + (df_std['E']**2/df_N['E']))

tstat = top/bottom
sig = tstat[np.abs(tstat) > 2]
sig.name = 't-stats'
sig

#-------------------------------------------------------------------
# Section II
#-------------------------------------------------------------------
##Create a dataframe with ID, treatment, weight (w) from propensity score
# 1) Get "p hat" for prob D=1. 
logit_results, df_logit = do_logit(df_pretrial, 'C', '4', add_D=None, mc=False)
df_logit['p_hat'] = logit_results.predict()
df_logit.head()

# 2) Get w, the weight (See Harding, 2013, page 4-10)
    ##Create a treatment variable
df_logit['treatment'] = 0 + (df_logit['tariff'] == 'C')
    # don't need: df_logit['1-D'] = 0 + (df_logit['tariff'] == 'E')
df_logit.head()

    # yes, you can do 1 - df['blah']:    w = np.sqrt((df_logit['treatment']/df_logit['p_hat']) + (df_logit['1-D']/(1- df_logit['p_hat'])))
df_logit['w'] = np.sqrt((df_logit['treatment']/df_logit['p_hat']) + ((1 - df_logit['treatment'])/(1- df_logit['p_hat'])))

# 3) Create a dataframe of just ID, treatment, and weight (w)
df_w = df_logit[['ID', 'treatment', 'w']]
df_w.head()
#--------------------------------------------------------------------
# Section III
#-------------------------------------------------------------------

# 1. Import data and demean function from "fe_functions.py"
df_long = pd.read_csv(root + "task_4_kwh_long.csv")
from fe_functions import *
df_long.head()

# 2. Merge data : Merged DataFrame is df2
df2 = pd.merge(df_long, df_w)

# 3 (i) Create treatment and trial interaction variable
df2['treat*tri'] = df2['treatment']*df2['trial']

# 3 (ii) Create log (kwh + 1) 
df2['log_kwh'] = (df2['kwh'] + 1).apply(np.log)

# 3(iii) Create a year-month variable, ym.
df2['month_string'] = np.array(["0" + str(v) if v < 10 else str(v) for v in df2['month']])
df2.head()
df2['ym'] = df2['year'].apply(str) + "_" + df2['month_string']

# 4 (i - vi) Set up regression variables from merged dataframe, df2
y = df2['log_kwh']
P = df2['trial']
TP = df2['treat*tri']
w = df2['w']
mu = pd.get_dummies(df2['ym'], prefix = 'ym').iloc[:, 1:-1]
X = pd.concat([P, TP, mu], axis=1)

# 5. Demean y and X using the demean function 

ids = df2['ID']
y = demean(y, ids)
X = demean(X, ids)
X.head()

# 6. Run the Fixed Effects model with and without weights. Do not add constant. 

# WITHOUT WEIGHTS
fe_model = sm.OLS(y, X) #linear probability model
fe_results = fe_model.fit() # get fitted values
print fe_results.summary()

# WITH WEIGHTS 
y = w*y
names = X.columns.values
X = np.array([x*w for (k, x) in X.iteritems()])
X = np.array([x*w for k, x in X.iteritems()])
np.array([v[1]*w for v in X.iteritems()])


k, v = (1, 2)
z = (1, 2)


X = X.T #transpose because the array created row vectors, not volumn vectors. 
X = DataFrame(X, columns = names)
X.head()

fe_w_model = sm.OLS(y, X)
fe_w_results = fe_w_model.fit()
print fe_w_results.summary()

# 7 Note - understanding the stats I'm actually doing  ??????????????


