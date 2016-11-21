#########################################################################
## Section 2                                                           ##
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

#1) Import data and change working directory.
   ## Set up pathing 
main_dir = "C:/Users/J/Desktop/data/"
root = main_dir + "final/"
sect2 = root + "section_2/"

    ## Change working directory
os.chdir(sect2)
from logit_functions import *

    ## Import data
df = pd.read_csv(sect2 + "final_kwh_w_dummies_wide.csv")
df = df.dropna(axis=0, how='any')

# 2) Run the do_logit function on pre-trial data to check for balance.
 ## Keep only pre-trial data 
df_drop = [v for v in df.columns if v.startswith("kwh_2010")]
df_pretrial = df.drop(df_drop, axis=1)

 ## Create tariffs/stimuli groups
tariffs = [v for v in df['tariff'].unique() if v != 'E']
stimulus = [v for v in df['stimulus'].unique() if v != 'E']
tariffs.sort()
stimulus.sort()

for i in tariffs:
    for j in stimulus:
        logit_results, df_logit = do_logit(df_pretrial, i, j, add_D=None, mc=False)

# 3) Do a "Quick Means Comparison" and a sample t-test "by hand" to compare B4 treatment to EE control, pre-trial
    ## Group by treatment group; Get mean consumption, standard deviation, and N
trt_grp = df_logit.groupby('tariff')
df_mean = trt_grp.mean().transpose()
df_std = trt_grp.std().transpose()
df_N = trt_grp.count().transpose().mean()

top = df_mean['B'] - df_mean['E']
bottom = np.sqrt((df_std['B']**2/df_N['B']) + (df_std['E']**2/df_N['E']))
tstat = top/bottom
sig = tstat[np.abs(tstat) > 2]
sig.name = 'Significant t-stats'
sig

print "\n\n\n"
print tstat
print "\n\n\n"

# PART B ----------------------------------------------------------------------
 ## Run a FE model, with and without weights. 
 
#1) Generate the propensity score weights. 
    ## Get predicted values of the logit model 
df_logit['p_hat'] = logit_results.predict() 

    ## Generate the weights, w
df_logit['trt'] = 0 + (df_logit['tariff'] == 'B') #Create treatment column, 0/1's
df_logit['w'] = np.sqrt(df_logit['trt']/df_logit['p_hat']) #Formula from Harding, 2013 paper
df_w = df_logit[['ID', 'trt', 'w']] #Create smaller dataframe with just ID, treatment, weights

# 2) Import the data and merge with the weights. 
df = pd.read_csv(sect2 + "final_kwh_long.csv")
df = pd.merge(df, df_logit)

# 3) Create the necessary variables to run FE model 
    ## Interaction dummy of treatment*trial
df['treat*tri'] = df['trt']*df['trial']
    ## Log of kwh consumption + 1
df['log_kwh'] = (df['kwh'] + 1).apply(np.log)
    ## A year-month categorical variable
df['mo_str'] = np.array(['0' + str(v) if v < 10 else v for v in df['month']])
df['ym'] = df['year'].apply(str) + "_" + df['mo_str']

df.head()

# 4) Set up the data for a fixed effects model, following Alcott, 2011. 
mu = pd.get_dummies(df['ym'], prefix = 'ym').iloc[:, 1:-1]
w = df['w']
y = df['log_kwh']
P = df['trial']
TP = df['treat*tri']
X = pd.concat([TP, P, mu], axis=1)

# 5) Run a fixed effects model WITHOUT weights.
    ## Import demeaning function
from fe_functions import *
    ## Demean y and X.
ids = df['ID']
y = demean(y, ids)
X = demean(X, ids)
X.head()

    ## FE model WITHOUT weights
fe_model = sm.OLS(y, X) 
fe_results = fe_model.fit()
print(fe_results.summary())

# 6) Run a fixed effects model WITH weights. 
    ## Apply weights to y, X
y_w = y*w
X_w = np.array([x*w for (k, x) in X.iteritems()])
X_w = X.transpose()
X.head()
names = X.columns.values
X_w = DataFrame(X, columns = names) #update X to dataframe; keep original names 

fe_w_model = sm.OLS(y_w, X_w) 
fe_w_results = fe_model.fit()
print(fe_w_results.summary())

print("------------------------------------ \n END OF SECTION 2 - WOOOHOOO!\n------------------------------------")










