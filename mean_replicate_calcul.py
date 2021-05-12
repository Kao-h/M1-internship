#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 09:53:10 2021

@author: kaouther
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
#path = '/home/kaouther/Documents/Internship/pre_process/input_files/heart_forKaouther.xlsx'
#path = '/home/kaouther/Documents/Internship/pre_process/input_files/tissues_9m_forKaouther3.xlsx'

path = '/home/kaouther/Documents/Internship/pre_process/input_files/clean/TabulaMuris_Senis_Brain.xlsx'
#path=input('enter the complete path to your input file')

#path = input('Paste the absolute path to the file') #enter the path to the heart_forKaouther.xlsx
#df = pd.read_csv(path, delimiter = "\t")
df = pd.read_excel(path)
#function de extract the  last caracterfrom a string
def get_rep_name(string):
    return (string[-1:])

#get columns names (samples & biological replicates)
column_names = df.columns
column_names = column_names.delete([0]) #remove gene

#get only biological replicates 
biological_rep=[]
mean_replicates= dict()
for name in column_names:
    if get_rep_name(name) not in biological_rep:
        #print(get_rep_name(name))
        biological_rep.append(name[-1:])
        
#dictionnary to store the sum of values of a  type of biological rep  and nb of iteration
for i in range (0,len(biological_rep),1): 
    mean_replicates['mean_replicate_'+biological_rep[i]] = [0]*len(df)
    mean_replicates['nb_itteration_'+biological_rep[i]] = [0]*len(df)
for k in range (0,len(df),1):
    
    for i in range (0, len(column_names),1):
        for j in biological_rep:
            if j in get_rep_name(column_names[i]):
                mean_replicates['mean_replicate_'+j][k]+= df.loc[k,column_names[i]]
                mean_replicates['nb_itteration_'+j][k]+=1


dico2 = dict()    #store tuples sum and iteration on each line
dico3 = dict()    #store the mean calculation 

for i in range (0,len(biological_rep),1):
    dico3['mean_replicate_'+biological_rep[i]] = [0]*len(df)

#get list of mean replicates
list_mean_replicates =[]
for i in range (0,len(biological_rep),1):
    list_mean_replicates.append('mean_replicate_'+biological_rep[i])
#dico to store as a tuple the sum and iteration for each mean rep
for key in list_mean_replicates:
    for key2 in mean_replicates:
        if key != key2 and get_rep_name(key) == get_rep_name(key2):
            print( key,key2)
            
            dico2[key]= list(zip((mean_replicates[key]),mean_replicates[key2]))
#dico to calculate the average per gene per mean replicate             
for key in dico2:
    for i in range(0,len(df),1):    
        cal =  round(dico2[key][i][0]/ dico2[key][i][1])
        dico3[key][i]= cal
#store results in new df in new columns
final_df = df.copy()
for mean in list_mean_replicates:
    final_df[mean] = 0
    
for i in range(0,len(final_df),1):
    for key in list_mean_replicates:
        final_df.loc[i,key] = dico3[key][i]
#export as excel the df 
final_df.to_excel ('/home/kaouther/Documents/Internship/pre_process/output_files/brain_matrix.xlsx', index = False, header=True)
#final_df.to_csv('/home/kaouther/Documents/Internship/pre_process/output_files/'+'tissues_mean.csv', index = False, header=True)
#final_df.to_excel('/home/kaouther/Documents/Internship/pre_process/output_files/'+'tissues_matrix.xlsx', index = False, header=True)
#file_name= input('file name')
#final_df.to_excel(file_name+'.xlsx', index = False, header=True)

duplicateRowsDF = final_df[final_df.iloc[:,0].duplicated()]
