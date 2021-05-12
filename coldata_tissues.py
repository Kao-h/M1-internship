#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 12:45:15 2021

@author: kaouther
"""


import pandas as pd
import re
path=input('enter the complete path to your input file')
#path ='/home/kaouther/Documents/Internship/pre_process/output_files/tissues_matrix.xlsx'
df = pd.read_excel(path)



#get columns names (samples & biological replicates)

columns = list(df.columns)

columns.remove('gene')



#extract the TP
age = columns[0].split('_')[1]


#create a sample list
samples_list=[]

for column in columns:
    match = re.search('[^0-9]+', column)
    if match:
        found = match.group()
        found = found.replace('_','')
        if found == 'meanreplicate':
             samples_list.append('mean')
        elif found == 'sample':
            continue
        else:
            samples_list.append(found)

#extract infos for the file directory
distinct_columns = []

[distinct_columns.append(age+'_'+x) for x in samples_list if age+'_'+x not in distinct_columns]
distinct_columns.remove(age+'_mean')
file_dico={}
liste = ["userID","sampleID","folder","subfolder","organism","datetime"]
for i in liste:
    file_dico[i]= []
for i in distinct_columns:
    file_dico["userID"].append('mitox')
    file_dico["sampleID"].append(i)
    file_dico["folder"].append('TabulaMuris')
    file_dico["subfolder"].append(age)
    file_dico["organism"].append("Mouse")
    file_dico["datetime"].append("20200208")
#export file directory   
df_file = pd.DataFrame.from_dict(file_dico)
path_directory_file= input('enter the path where to store the file')
df_file.to_csv (path_directory_file+'/file_directory_'+age+'.csv',index= False)       

#df_file.to_csv ('/home/kaouther/Documents/Internship/DEG/TP_heart/file_directory_'+age+'.csv',index= False)       

    
data_tuples = list(zip(columns,samples_list))
#export as df the metadata
df2 = pd.DataFrame(data_tuples, columns=['','tissues'])
df2['Name']=df2.iloc[:,0]

#export as xls
path_coldata=input('where to store the coldatafile')
df2.to_excel (path_coldata+'/tissues_coldata.xlsx', index = False, header=True)
#df2.to_excel ('/home/kaouther/Documents/Internship/pre_process/output_files/tissues_coldata.xlsx', index = False, header=True)