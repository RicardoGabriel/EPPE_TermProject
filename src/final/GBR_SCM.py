"""
Created on Mon Feb  11 14:08:09 2019
@author: Ricardo Duque Gabriel

The file GBR_SCM.py has the code for the creation of a SCG for Japanese GDP series using 31 OECD countries and 
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
#leaving Great Britain out (code==GBR) index:13
control_units = control_units[0:13]+control_units[14:]


#define which predictors to use
predictors = ["pc_gdp_s", "unemp", "pc_govcons_s", 
             ]

#define initial educated guess for weights - following Born et al. (2018)
weights=np.array([0,0,0,0.16,0,0,0,0,0,0,0,0,0,0.21,0.00,0,0,0.04,0.24,0.03,0,0,0,0,0,0.04,0,0,0.06,0,0,0.22]).transpose()

#create synth tables
Weights=synth_tables(  df,
               predictors,
               "GBR",
               control_units,
               "code",
               "pc_gdp_s",
               weights,
               "time",
               [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86],
               [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86],
               [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95]
               )

plt.savefig(ppj("OUT_FIGURES",'Synthetic_Control_Method_GBR.png'))

Weights.to_pickle(ppj("OUT_TABLES", 'Weights_GBR.pkl'))