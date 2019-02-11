"""
Created on Sun Feb  3 14:08:09 2019
@author: Ricardo Duque Gabriel

Code for the creation of a SCG for Japanese GDP series  
using 31 OECD countries to be our donor pool
"""

import pandas as pd
import matplotlib.pyplot as plt
import synth
#from bld.project_paths import project_paths_join as ppj

#import excel dataset to panda dataframe
#df = pd.read_excel(ppj("IN_DATA",'Dataset_TermPaper.xlsx'), header=0).iloc[:3135]
df = pd.read_excel('Dataset_TermPaper.xlsx', header=0).iloc[:3135]


#define control units
control_units = list(set(df["code"]))
control_units.sort()
#leaving Japan out (code==JPN) 
control_units = control_units[0:19]+control_units[20:32]


#define which predictors to use
predictors = ["pc_gdp_s",
             ]

#define initial educated guess for weights - following Born et al. (2018)
weights=np.array([1/len(control_units)]*len(control_units)).transpose() #equal weights



#create synth tables
synth_tables(  df,
               predictors,
               "JPN",
               control_units,
               "code",
               "pc_gdp_s",
               weights,
               "time",
               [1,2,3,4,5,6,7,8],
               [1,2,3,4,5,6,7,8],
               [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
               )


#debugging
#foo=df
#treated_unit="JPN"
#index_variable="code"
#measured_variable="pc_gdp_s"
#time_variable="time"
#predict_time=[1,2,3,4,5,6,7,8]
#optimize_time=[1,2,3,4,5,6,7,8]
#plot_time=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
#function="mean"