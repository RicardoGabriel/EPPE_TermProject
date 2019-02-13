"""
Created on Sun Feb  3 14:08:09 2019
@author: Ricardo Duque Gabriel 

The file Japan_SCM.py has the code for the creation of a SCG for Japanese GDP series using 31 OECD countries and 
saves the plot of both synthtetic and original series.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from src.library.synth import synth_tables
from bld.project_paths import project_paths_join as ppj

#import excel dataset to panda dataframe
df = pd.read_excel(ppj("IN_DATA",'Dataset_TermPaper.xlsx'), header=0).iloc[:3135]

#define control units
control_units = list(set(df["code"]))
control_units.sort()
#leaving Japan out (code==JPN) index:19
control_units = control_units[0:19]+control_units[20:32]


#define which predictors to use
predictors = ["pc_gdp_s",
             ]

#define initial educated guess for weights - all countries have equal weight
weights=np.array([1/len(control_units)]*len(control_units)).transpose()

#create synth tables
Weights=synth_tables(  df,
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

plt.savefig(ppj("OUT_FIGURES",'Synthetic_Control_Method_Japan.png'))

Weights.to_pickle(ppj("OUT_TABLES", 'Weights_Japan.pkl'))