"""
Created on Sun Feb 10 14:08:09 2019
@author: Ricardo Duque Gabriel

Data Management - from Excel to pkl
"""

import pandas as pd
from bld.project_paths import project_paths_join as ppj

#import excel dataset to panda dataframe

df = pd.read_excel(ppj("IN_DATA",'Dataset_TermPaper.xlsx'), header=0).iloc[:3360]


#transform variable 'year' to one integer time variable
x=1
for i in range(0,3360):
    df.year[i]=x
    x=x+1
    if x==97:
        x=1


df = df[df.gdp_s.notnull()]
df.drop(["unemp", "peg"], axis = 1, inplace = True) 
#df.to_pickle('dataset.pkl')

df.tofile(ppj("OUT_DATA", "dataset.csv"), sep=",")
