#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 20:39:43 2025

@author: sonalgupta
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics as stats
from itertools import combinations

folder_path = '/Users/sonalgupta/Downloads/ETF/'

df_b = pd. read_parquet(folder_path+'XLB_1min.parquet')
df_c = pd. read_parquet(folder_path+'XLC_1min.parquet')
df_e = pd. read_parquet(folder_path+'XLE_1min.parquet')
df_f = pd. read_parquet(folder_path+'XLF_1min.parquet')

def data_filter(df):
    # description: this function makes all time series of equal length 'n_elts'
    #              It selects the first n_elt elements of each time series  
    # input: multiple time series arranged in columns. one time series per column
    # output: all time series pruned to minimum linght of a time series of all the series
    L= []
    for j in range(len(df)):
        L.append((df[j]).size)
    n_elts = min(L)
    for j in range(len(df)):
        df[j] = df[j][0:n_elts-1]
    return df  


unique_dates_df_b = np.unique(df_b.index.date)
unique_dates_df_c = np.unique(df_c.index.date)
unique_dates_df_e = np.unique(df_e.index.date)
unique_dates_df_f = np.unique(df_f.index.date)

fltrd_dates_bc = np.intersect1d(unique_dates_df_b, unique_dates_df_c,assume_unique=False, return_indices=True)
fltrd_dates_be = np.intersect1d(unique_dates_df_b, unique_dates_df_e,assume_unique=False, return_indices=True)
fltrd_dates_bf = np.intersect1d(unique_dates_df_b, unique_dates_df_f,assume_unique=False, return_indices=True)
fltrd_dates_ce = np.intersect1d(unique_dates_df_c, unique_dates_df_e,assume_unique=False, return_indices=True)
fltrd_dates_cf = np.intersect1d(unique_dates_df_c, unique_dates_df_f,assume_unique=False, return_indices=True)
fltrd_dates_ef = np.intersect1d(unique_dates_df_e, unique_dates_df_f,assume_unique=False, return_indices=True)




clm_names = []
for  i in df_b.columns:
    clm_names.append(i)
cmb_clms = combinations([0,1,2,3,4], 2)
#cmb_clms = zip(range(5),range(5))


def corr_calc(clm_names,cmb_clms,df_1,df_2,fltrd_dates):
    xc_med_corr = []
    corr_all = []
    for j in cmb_clms:
        print(clm_names[j[0]])
        print(clm_names[j[1]])
      
        corr_population = []
        for i in fltrd_dates[2]:
        
            df1 = df_1.loc[(str(fltrd_dates[0][i].year)+'-'+str(fltrd_dates[0][i].month)+'-'+str(fltrd_dates[0][i].day)),clm_names[j[0]]]
            df2 = df_2.loc[(str(fltrd_dates[0][i].year)+'-'+str(fltrd_dates[0][i].month)+'-'+str(fltrd_dates[0][i].day)),clm_names[j[1]]]
            df = [df1,df2]
            L = data_filter(df)
            corr_candidates = [clm_names[j[0]],clm_names[j[1]]]
            corr_dict = dict(zip(corr_candidates,L))
            corr_df = pd.DataFrame.from_dict(corr_dict,orient='columns')
            corr_coef = corr_df.corr()
            corr_population.append(corr_coef.loc[clm_names[j[0]],clm_names[j[1]]])
            
        corr_all.append(list(filter(lambda x: ~np.isnan(x),corr_population)))
        xc_med_corr.append((stats.median(corr_population),clm_names[j[0]],clm_names[j[1]]))
        
    return corr_all, xc_med_corr

# [corr_population_bc,xc_med_corr_bc] = corr_calc(clm_names,cmb_clms,df_b,df_c,fltrd_dates_bc)
# plt.boxplot(corr_population_bc,labels = ['o-h','o-l','o-c','o-vol','h-l','h-c','h-vol','l-c','l-vol','c-vol'])
# plt.title('correlation bc')

# [corr_population_be,xc_med_corr_be] = corr_calc(clm_names,cmb_clms,df_b,df_e,fltrd_dates_be)
# plt.boxplot(corr_population_be,labels = ['o-h','o-l','o-c','o-vol','h-l','h-c','h-vol','l-c','l-vol','c-vol'])
# plt.title('correlation be')

# [corr_population_bf,xc_med_corr_bf] = corr_calc(clm_names,cmb_clms,df_b,df_f,fltrd_dates_bf)
# plt.boxplot(corr_population_bf,labels = ['o-h','o-l','o-c','o-vol','h-l','h-c','h-vol','l-c','l-vol','c-vol'])
# plt.title('correlation bf')

# [corr_population_ce,xc_med_corr_ce] = corr_calc(clm_names,cmb_clms,df_c,df_e,fltrd_dates_ce)
# plt.boxplot(corr_population_ce,labels = ['o-h','o-l','o-c','o-vol','h-l','h-c','h-vol','l-c','l-vol','c-vol'])
# plt.title('correlation ce')

# [corr_population_cf,xc_med_corr_cf] = corr_calc(clm_names,cmb_clms,df_c,df_f,fltrd_dates_cf)
# plt.boxplot(corr_population_cf,labels = ['o-h','o-l','o-c','o-vol','h-l','h-c','h-vol','l-c','l-vol','c-vol'])
# plt.title('correlation cf')

[corr_population_ef,xc_med_corr_ef] = corr_calc(clm_names,cmb_clms,df_e,df_f,fltrd_dates_ef)
plt.boxplot(corr_population_ef,labels = ['o-h','o-l','o-c','o-vol','h-l','h-c','h-vol','l-c','l-vol','c-vol'])
plt.title('correlation ef')



#plt.show()  
#plt.boxplot(corr_population_bf)    

# df_b_o = df_b.loc['2017-01-03','tpxo']
# #df_c_o = df_c.loc['2017-01-03','tpxo']
# df_e_o = df_e.loc['2017-01-03','tpxo']
# df_f_o = df_f.loc['2017-01-03','tpxo']



# plt.plot(df_b_o/((df_b_o.abs()).max()))
# plt.plot(df_e_o/((df_e_o.abs()).max()))
# plt.plot(df_f_o/((df_f_o.abs()).max()))
# plt.xlabel('time')
# plt.ylabel('normalized param')
# plt.title('opening')
    
# plt.show()

# df = [df_b_o, df_e_o,df_f_o]
# L = data_filter(df)

# corr_candidates = ['b_o','e_o','f_o']
# corr_dict = dict(zip(corr_candidates,df))
# corr_df = pd.DataFrame.from_dict(corr_dict,orient='columns')
# corr_coef = corr_df.corr()
# print(corr_coef)
                 
        
    