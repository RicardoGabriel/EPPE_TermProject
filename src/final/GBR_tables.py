"""
Created on Wed Feb  13 9:33:18 2019
@author: Ricardo Duque Gabriel

Code for the creation of a Table in latex with the composition (in weights) of the doppelganger of the United Kingdom.
"""
#This sucks, but I could not find any easy-to-implement solution ...


import pandas as pd
from bld.project_paths import project_paths_join as ppj
from tabulate import tabulate
from math import ceil, floor
def float_round(num, places = 0, direction = floor):
    return direction(num * (10**places)) / float(10**places)

#import pickle with information on weights
Weights=pd.read_pickle(ppj("OUT_TABLES", 'Weights_GBR.pkl'))

#check how many rows you need to get a 8 column table
y=ceil(len(Weights)/4)

#create the dataframe for the new table
df = pd.DataFrame(index=range(y+1),columns=range(8))

#fill in the new dataframe
l=0
for i in range(0, 8, 2):
    for j in range(1, y+1):
        df.iloc[j,i]=Weights.index[l]
        l=l+1
        if l==len(Weights):
            break
l=0
for i in range(1, 8, 2):
    for j in range(1, y+1):
        df.iloc[j,i]=float_round(Weights.iloc[l,0], 3, round)
        l=l+1
        if l==len(Weights):
            break
        
#Get headers right
for i in range(0,8,2):
    df.iloc[0,i]='Country'
    
for i in range(1,8,2):
    df.iloc[0,i]='Weight'

print(tabulate(df, showindex="never", headers="firstrow", tablefmt="latex_booktabs", floatfmt=".3f"))

with open("Table_GBR.tex","w") as tf:
     tf.write(ppj("OUT_TABLES", df.to_latex(index=False, header=False, na_rep='', float_format=str)))