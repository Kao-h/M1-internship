#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 11:52:35 2021

@author: kaouther
"""


import pandas as pd
import re


#path=input('enter the complete path to your input file')
#path ='/home/kaouther/Documents/Internship/pre_process/output_files/heart_mean.xlsx'
path ='/home/kaouther/Documents/Internship/pre_process/output_files/brain_matrix.xlsx'

df = pd.read_excel(path)



#get columns names (samples & biological replicates)

columns = list(df.columns)
columns.remove('gene')



distinct_columns = [] 
for column in columns:
    if column[:-3] not in distinct_columns and column[:-3].endswith("m"):
        distinct_columns.append(column[:-3])
        
tissue= columns[0].split('_')[0]


#extract infos for the file directory
file_dico={}
liste = ["userID","sampleID","folder","subfolder","organism","datetime"]
for i in liste:
    file_dico[i]= []
for i in distinct_columns:
    file_dico["userID"].append('mitox')
    file_dico["sampleID"].append(i)
    file_dico["folder"].append('TabulaMuris_senis')
    file_dico["subfolder"].append(tissue)
    file_dico["organism"].append("Mouse")
    file_dico["datetime"].append("20200208")
#export
df_file = pd.DataFrame.from_dict(file_dico)
df_file.to_csv ('/home/kaouther/Documents/Internship/DEG/TP_heart/file_directory_'+tissue+'.csv',index= False)
    


#create a sample list
samples_list=[]

for column in columns:
    match = re.search('_..+_', column)
    if match:
        found = match.group()
        found = found.replace('_','')
        if found == 'replicate':
             samples_list.append('mean')
        else:
            samples_list.append(found)
    elif column == 'sample':
        continue
        
    
data_tuples = list(zip(columns,samples_list))
#export as df 
df2 = pd.DataFrame(data_tuples, columns=['','age'])
df2['Name']=df2.iloc[:,0]

#export as xls
#df2.to_excel ('/home/kaouther/Documents/Internship/pre_process/output_files/heart_coldata.xlsx', index = False, header=True)
df2.to_excel ('/home/kaouther/Documents/Internship/DEG/TP_'+tissue+'/'+tissue+'_coldata.xlsx', index = False, header=True)