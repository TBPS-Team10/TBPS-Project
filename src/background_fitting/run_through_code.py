# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 14:27:25 2023

@author: Louis Beucher
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import model_XGB
import angular_background_Cheb_fits as cbaf
from acceptance_legendre_background import acceptance_legendre_2
import Finalised_filters as Ff
from acceptance_new_2 import acceptance_legendre_new_2
#%%
# add any additional file names you wish to use. Not using jpsi and psi2S as assuming they are already fully filtered out
filenames = ["Jpsi_Kstarp_pi0.csv", "jpsi_mu_k_swap.csv",
             "jpsi_mu_pi_swap.csv", "k_pi_swap.csv", "Kmumu.csv", "Kstarp_pi0.csv",
             "phimumu.csv", "pKmumu_piTok_kTop.csv", "pKmumu_piTop.csv","jpsi.csv","psi2S.csv"]
#keeping correct order is important
sig=pd.read_csv('../data/sig.csv',delimiter=',')
tot_data=pd.read_csv('../data/total_dataset.csv',delimiter=',',dtype='float32')
column_headers = list(sig.columns.values)
acceptance_data=pd.read_csv('../data/acceptance_mc.csv',delimiter=',',dtype='float32')
acceptance_data=acceptance_data.reindex(columns=column_headers)
#%% filter out the data using the ML
def ML_filtering(df):
    feature_list=np.loadtxt('ML model/filters_24.02.2023_features_20_depth_3_estimators_200_feature_list.csv',delimiter=',',dtype='int32')

    bdt_model=model_XGB.BDT_model()
    bdt_model.load_model("ML model/filters_24.02.2023_features_20_depth_3_estimators_200.json")
    bdt_model.specify_feature_num(20)
    bdt_model.specify_features(feature_list)
    y_test=bdt_model.predict(np.array(df))
    
    df.drop(df[y_test!=0].index, inplace=True)
    return np.array(df)

#%% using finalised filter to filter out the simulated dataset for chebyshev fits
for name in filenames:
    data = pd.read_csv(f"../data/{name}", delimiter=",",dtype='float32') #load datafile, add ./data if required 
    print('initial length',len(data))
    Ff.filter_light(sig,data) #select data using filtering method, filtering method may be changed
    ML_filtering(data) #using the ML to filter too
    print('length after filtering',len(data))
    if name=="Jpsi_Kstarp_pi0.csv":
        tot_filtered_data=data
    else:
        tot_filtered_data=pd.concat([tot_filtered_data,data],ignore_index=True)
        
print('the length of the combined filtered simulated datasets is:',len(tot_filtered_data))
#%% filtering acceptance and total dataset
print(f'initial length of acceptance is {len(acceptance_data)} ') 
Ff.filter_light(sig,acceptance_data)
print(f'length of acceptance after filtering is {len(acceptance_data)}')
print(f'initial length of total dataset is {len(tot_data)} ') 
Ff.filter_light(sig,tot_data)
print(f'length of total dataset after filtering is {len(tot_data)}')

#%% ML filtering acceptance and total dataset
print(f'length of acceptance before ML filtering is {len(acceptance_data)}')
filtered_acceptance=ML_filtering(acceptance_data)
print(f'length of acceptance after ML filtering is {len(acceptance_data)}')
print(f'length of total dataset before ML filtering is {len(tot_data)}')
tot_dataset_filtered=ML_filtering(tot_data)
print(f'length of total dataset after ML filtering is {len(tot_data)}')


#%% separation into bins for all_fits calculation
all_bins=cbaf.bin_separation(tot_filtered_data)
#%%
# finding all the fits coefficients
all_fits=cbaf.fit_all_bins(all_bins, 2,plot=True)

#%%

q2_bins=[[0,1,0.98],[1.1,2.5],[2.5,4.0],[4.0,6.0],[6.0,8.0],[15.0,17.0],[17.0,19.0],[11.0,12.5],[1.0,6.0],[15.0,19.0]]
#%%
everything=acceptance_legendre_2(filtered_acceptance,q2_bins, all_fits,order_costhetal=5, order_costhetak=5, order_phi=6)


SM_fits=[0]*len(all_bins)
for i in range(0,10):
    
    SM_fits[i]=everything.fit_SM_observables(tot_dataset_filtered,i)
    print(f'SM fits returned for bin {i}')
    

#%% saving the newly obtained fits
for i in range (0,10):
    np.savetxt(f'SM_fits_data/SM_fits_bin_{i}.csv',SM_fits[i],delimiter=',')

#%% trying the fits with the new normalisation for bin 0
sm_fit_func_b=acceptance_legendre_new_2(filtered_acceptance,q2_bins, all_fits, order_costhetal=4, order_costhetak=5, order_phi=6)

guess=[0.3,-0.1,0.01,0.1,0.25,-0.02,-0.002,-0.0007,0.3]

SM_fits_1bin=sm_fit_func_b.fit_SM_observables_integral(tot_dataset_filtered, 0, guess, intervals=140)
print('SM fits returned')




