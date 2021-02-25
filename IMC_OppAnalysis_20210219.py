# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 17:04:09 2021

@author: Giancarlo
"""

######################### Opportunity Analysis ############################ 
#script will be used to build python based containerized lambda functions

#read ICD and CPT code associations/groupings
import pandas as pd

### CPT ###
CPT = pd.read_csv("MSK_CPT_DRG_REV-20210109-15-WSM.csv")

### ICD ###
ICD = pd.read_csv("MSK_ICD_Codes-20210211-15-WSM.csv")

### D ###
# Excel file should open outside of Spyder 
# and ask for password after running code
# Once password entered, "D" dataframe is created 
import xlwings as xw
path = 'Small_SIMdata_for Testing-20210217-01-WSM.xlsx'
wb = xw.Book(path)
sheet = wb.sheets['Sheet2']
D = sheet['A1:F41542'].options(pd.DataFrame,index = False, Header = True).value 

# Match the ICD in D to reference list BRalias
D['BRALIAS'] = ICD['BRALIAS'].loc[ICD['Dx'].isin(D['DX'])]
    #D['test'] = ICD['BRALIAS'].loc[D['DX'].isin(ICD['Dx'])]
D['BRALIAS'].value_counts() # R funciton Table() equivalent

# create BRID
D['BRID'] = D['EMID'] +'-'+ D['BRALIAS']

### MAXPL for MSD ###
# Remove NA's and subset BRalias to find MSD's MaxPL
D1 = D.dropna(subset=['BRALIAS'])
D1.value_counts() #Review

# Match PX in D to refrence list CPT
D1['PL'] = CPT['PL'].loc[CPT['Code'].isin(D1['PCode'])]
D1['PL'].value_counts() #Review

# D1['test'] = CPT['PL'].loc[D1['PCode'].isin(CPT['Code'])]
# returns "IndexingError" 
# Attempted to fix using .reset_index() when creating D1 (line 40) 

# Aggregate to build maxPL reference
MaxPL = D1.groupby('PL')['BRID'].max()
MaxPL.head() #Review

# Subset the balance of rows
D2 = D.dropna(subset=['BRALIAS'])
len(D2['BRID']) #556

# Create "NA" MaxPL/PL for balance on D2
# Create PL class for D2
# Create inverted min PL class for D2

D2[['MaxPL','PL','PLclass','minPL']] = 'NA'

# Recombine
D = pd.concat([D1, D2]) 

#output lambda function to...
D.to_csv("CLIENT_Processed-20201001-01-WSM_PythonBased.csv")

#End of File



