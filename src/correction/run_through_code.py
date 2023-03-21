# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 14:27:25 2023

@author: Louis Beucher
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import Selection_criteria_func #need the filtering file in the same directory
import model_XGB
import angular_background_Cheb_fits as cbaf
from acceptance_legendre_2 import acceptance_legendre_2
from acceptance_legendre import acceptance_legendre
import Finalised_filters as Ff
from acceptance_new import acceptance_legendre_new
from acceptance_new_2 import acceptance_legendre_new_2
from acceptance_new_forced import acceptance_legendre_new_3
from scipy.stats import chi2
#%%
plt.style.use("bmh")

plt.rcParams.update({
    "figure.figsize": (8, 5),
    "font.serif": ["Times New Roman"],
    "legend.fontsize": 18,
    "axes.labelsize": 20,
    "axes.titlesize": 18,
    "xtick.labelsize": 18,
    "ytick.labelsize": 18,
    "font.family": "serif"})
#%%
# add any additional file names you wish to use. Not using jpsi and psi2S as assuming they are already fully filtered out
filenames = ["Jpsi_Kstarp_pi0.csv", "jpsi_mu_k_swap.csv",
             "jpsi_mu_pi_swap.csv", "k_pi_swap.csv", "Kmumu.csv", "Kstarp_pi0.csv",
             "phimumu.csv", "pKmumu_piTok_kTop.csv", "pKmumu_piTop.csv","jpsi.csv","psi2S.csv"]
#keeping correct order is important
sig=pd.read_csv('data/sig.csv',delimiter=',')
tot_data=pd.read_csv('data/total_dataset.csv',delimiter=',',dtype='float32')
column_headers = list(sig.columns.values)
acceptance_data=pd.read_csv('data/acceptance_mc.csv',delimiter=',',dtype='float32')
acceptance_data=acceptance_data.reindex(columns=column_headers)
#%%
def ML_filtering(df):
    feature_list=np.loadtxt('ML model/filters_24.02.2023_features_20_depth_3_estimators_200_feature_list.csv',delimiter=',',dtype='int32')

    bdt_model=model_XGB.BDT_model()
    bdt_model.load_model("ML model/filters_24.02.2023_features_20_depth_3_estimators_200.json")
    bdt_model.specify_feature_num(20)
    bdt_model.specify_features(feature_list)
    y_test=bdt_model.predict(np.array(df))
    
    df.drop(df[y_test!=0].index, inplace=True)
    return np.array(df)

#%% using aisulu's filter, only choose one of the filtering cells
for name in filenames:
    data = pd.read_csv(f"data/{name}", delimiter=",",dtype='float32') #load datafile, add ./data if required 
    print('initial length',len(data))
    Ff.filter_light(sig,data) #select data using filtering method, filtering method may be changed
    ML_filtering(data) 
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

#%% finding all the fits coefficients
all_fits=cbaf.fit_all_bins(all_bins, 2,plot=True)

#%%

q2_bins=[[0,1,0.98],[1.1,2.5],[2.5,4.0],[4.0,6.0],[6.0,8.0],[15.0,17.0],[17.0,19.0],[11.0,12.5],[1.0,6.0],[15.0,19.0]]


    
#%%
'''
everything=acceptance_legendre_2(filtered_acceptance,q2_bins, all_fits,order_costhetal=5, order_costhetak=5, order_phi=6)


SM_fits=[0]*len(all_bins)
for i in range(0,10):
    
    SM_fits[i]=everything.fit_SM_observables(tot_dataset_filtered,i)
    print(f'SM fits returned for bin {i}')
    
#%% trying with no background

everything_no=acceptance_legendre(filtered_acceptance,q2_bins,order_costhetal=5, order_costhetak=5, order_phi=6)

SM_fits_no=[0]*10
for i in range(0,10):
    
    SM_fits_no[i]=everything_no.fit_SM_observables(np.array(tot_dataset_filtered),i)
    print(f'SM fits returned for bin {i}')
    
#%%
for i in range (0,10):
    np.savetxt(f'data/output_data/SM_fits_2/SM_fits_bin_{i}.csv',SM_fits[i],delimiter=',')

#%% separating data tot filtered data into bins and function to plot
bins_tot=cbaf.bin_separation(tot_data)
def PDF(cos_l,cos_k,phi,F_L, A_FB, S3, S4, S5, S7, S8, S9):
    cos_squared_k = cos_k**2
    cos_2l = 2. * cos_l**2 - 1.
    cos_phi = np.cos(phi)
    cos_2phi = np.cos(2. * phi)
    sin_squared_l = 1. - cos_l**2
    sin_squared_k = 1. - cos_squared_k
    sin_l = np.sqrt(sin_squared_l)
    sin_k = np.sqrt(sin_squared_k)
    sin_2l = 2. * sin_l * cos_l
    sin_2k = 2. * sin_k * cos_k
    sin_phi = np.sin(phi)
    sin_2phi = np.sin(2. * phi)
    
    func_vals = 0.75 * (1. - F_L) * sin_squared_k
    func_vals += F_L * cos_squared_k
    func_vals += 0.25 * (1. - F_L) * sin_squared_k * cos_2l
    func_vals -= F_L * cos_squared_k * cos_2l
    func_vals += S3 * sin_squared_k * sin_squared_l * cos_2phi
    func_vals += S4 * sin_2k * sin_2l * cos_phi
    func_vals += S5 * sin_2k * sin_l * cos_phi
    func_vals += (4./3.) * A_FB * sin_squared_k * cos_l
    func_vals += S7 * sin_2k * sin_l * sin_phi
    func_vals += S8 * sin_2k * sin_2l * sin_phi
    func_vals += S9 * sin_squared_k * sin_squared_l * sin_2phi
    func_vals *= (9./32.) * np.pi
    return func_vals
#%% plotting results at constant k and phi
ang_var='costhetal'
bin_num=20

for i in range(0,len(bins_tot)):
    cos_l = np.linspace(-1,1,200)
    cos_k = np.ones((200))
    phi = np.pi*np.ones((200))
    variable=cos_l # change this if necessary
    
    background=cbaf.create_background_pdf(cos_l,cos_k,phi,all_fits,i)
    
    fit_coeffs_background=np.loadtxt(f'data/output_data/SM_fits_b/SM_fits_bin_{i}.csv',delimiter=',')
    fit_coeffs=np.loadtxt(f'data/output_data/SM_fits/SM_fits_bin_{i}.csv',delimiter=',')
    
    fitted_PDF=PDF(cos_l,cos_k,phi,*fit_coeffs[:,0])
    fitted_PDF_b=fit_coeffs_background[8,0]*PDF(cos_l,cos_k,phi,*fit_coeffs_background[0:8,0])+(1-fit_coeffs_background[8,0])*background
    plt.figure(i)
    plt.plot(variable,fitted_PDF,color='red',label='fitted PDF without background')
    plt.plot(variable,fit_coeffs_background[8,0]*background,color='blue',label='background')
    plt.plot(variable,fitted_PDF_b,color='green',label='fitted PDF with background')
    plt.xlabel(ang_var)
    plt.ylabel('PDF')
    plt.legend()
    plt.grid()
    plt.show()

#%% trying with the new acceptance_legendre
sm_fit_func=acceptance_legendre_new(filtered_acceptance,q2_bins, order_costhetal=4, order_costhetak=5, order_phi=6)

guess=[0.3,-0.1,0.01,0.1,0.25,-0.02,-0.002,-0.0007]

SM_fits_1bin_no=sm_fit_func.fit_SM_observables_integral_bootstrap(tot_dataset_filtered, 0, guess, bootstrap_number=5, intervals=140)
print('SM fits returned')

#%% trying ot addd background into it
sm_fit_func_b=acceptance_legendre_new_2(filtered_acceptance,q2_bins, all_fits, order_costhetal=4, order_costhetak=5, order_phi=6)

guess=[0.3,-0.1,0.01,0.1,0.25,-0.02,-0.002,-0.0007,0.95]

SM_fits_1bin=sm_fit_func_b.fit_SM_observables_integral(tot_dataset_filtered, 0, guess, intervals=140)
print('SM fits returned')


#%%
sm_fit_func_b=acceptance_legendre_new_3(filtered_acceptance,q2_bins, all_fits, 0.093, order_costhetal=4, order_costhetak=5, order_phi=6)

guess=[0.30,-0.097,0.01,0.09,0.25,-0.02,-0.002,-0.0007]

SM_fits_forced=sm_fit_func_b.fit_SM_observables_integral(tot_dataset_filtered, 0, guess, intervals=140)
print('SM fits returned')

#%%
sm_fit_func_b=acceptance_legendre_new_3(filtered_acceptance,q2_bins, all_fits, 0.093, order_costhetal=4, order_costhetak=5, order_phi=6)

guess=[0.30,-0.097,0.01,0.09,0.25,-0.02,-0.002,-0.0007]

SM_fits_forced_b=sm_fit_func_b.fit_SM_observables_integral_bootstrap(tot_dataset_filtered, 0, guess, bootstrap_number=5, intervals=140)
print('SM fits returned')
'''
#%% running the bootstrap for 100 times with background
acq_params=pd.read_csv("data/params/acq_params.csv",delimiter=',',dtype='int')
SM_guesses=pd.read_csv("data/params/SM_guesses.csv",delimiter=',',dtype='float32')
acq_params=np.array(acq_params)
SM_guesses=np.array(SM_guesses)

for i in range(5,10):
    
    params=acq_params[i,:]
    sm_fit_func=acceptance_legendre_new_3(filtered_acceptance,q2_bins, all_fits, 0.093, order_costhetal=params[0], order_costhetak=params[1], order_phi=params[2])
    guess=SM_guesses[:,i]
    SM_fits_forced=sm_fit_func.fit_SM_observables_integral_bootstrap(tot_dataset_filtered, i, guess, bootstrap_number=50, intervals=params[3])
    print(f'bin {i} finished')
    np.savetxt(f'data/bootstrap_results2/bin_{i}.csv',SM_fits_forced,delimiter=',')
    
    

    
#%% filtering the datasets from bootstrapping and finding means and errors in final SM values#
'''
SM_theory=pd.read_csv("data/params/SM_guesses.csv",delimiter=',',dtype='float32')
conv_perc=np.zeros(10)
F_L=np.zeros((10,2))
A_FB=np.zeros((10,2))
S_3=np.zeros((10,2))
S_4=np.zeros((10,2))
S_5=np.zeros((10,2))
S_7=np.zeros((10,2))
S_8=np.zeros((10,2))
S_9=np.zeros((10,2))


for i in [1,3]:
    SM_values=np.loadtxt(f'data/bootstrap_results2/bin_{i}.csv',delimiter=',')
    conv=np.zeros(100)
    guess=0.9#SM_theory[f'{i}'][0]
    for j in range(0,100):
        conv[j]=np.allclose(SM_values[j,0],guess)
    
    SM_values=SM_values[np.logical_not(conv==1),:]
    if i==1:
        print(SM_values[:,0])
        
    conv_perc[i]=len(SM_values)
    
   
    F_L[i,0]=np.mean(SM_values[:,0])
    F_L[i,1]=np.std(SM_values[:,0])
    A_FB[i,0]=np.mean(SM_values[:,1])
    A_FB[i,1]=np.std(SM_values[:,1])
    S_3[i,0]=np.mean(SM_values[:,2])
    S_3[i,1]=np.std(SM_values[:,2])
    S_4[i,0]=np.mean(SM_values[:,3])
    S_4[i,1]=np.std(SM_values[:,3])
    S_5[i,0]=np.mean(SM_values[:,4])
    S_5[i,1]=np.std(SM_values[:,4])
    S_7[i,0]=np.mean(SM_values[:,5])
    S_7[i,1]=np.std(SM_values[:,5])
    S_8[i,0]=np.mean(SM_values[:,6])
    S_8[i,1]=np.std(SM_values[:,6])
    S_9[i,0]=np.mean(SM_values[:,7])
    S_9[i,1]=np.std(SM_values[:,7])


np.savetxt('data/SM_values_bootstrap2/F_L.csv',F_L,delimiter=',')    
np.savetxt('data/SM_values_bootstrap2/A_FB.csv',A_FB,delimiter=',')  
np.savetxt('data/SM_values_bootstrap2/S_3.csv',S_3,delimiter=',')  
np.savetxt('data/SM_values_bootstrap2/S_4.csv',S_4,delimiter=',')  
np.savetxt('data/SM_values_bootstrap2/S_5.csv',S_5,delimiter=',')  
np.savetxt('data/SM_values_bootstrap2/S_7.csv',S_7,delimiter=',')  
np.savetxt('data/SM_values_bootstrap2/S_8.csv',S_8,delimiter=',')  
np.savetxt('data/SM_values_bootstrap2/S_9.csv',S_9,delimiter=',')  
np.savetxt('data/SM_values_bootstrap2/convergence_percentage.csv',conv_perc,delimiter=',')  



#%% chi2 of Chebyshev for bin 8 

angular_variables=['costhetal','costhetak','phi']
p_values=np.zeros(3)
for i in range(0,3):
    fit_dat=all_fits[8][i][2]
    freq,bin_edges=np.histogram(all_bins[8][angular_variables[i]],bins=10,density=True)
    freq2,bin_egdes2=np.histogram(all_bins[8][angular_variables[i]],bins=10,density=False)
    err=np.sqrt(freq2)*freq/freq2
    chi_2=np.sum( ( (freq-fit_dat) / err )**2 )
    p_values[i]=1-chi2.cdf(chi_2,9)


#%% trying to find potnetial cp violation 
#separating into particles and antiparticles
part=tot_dataset_filtered[tot_dataset_filtered[:,86]==511]
acc=filtered_acceptance[filtered_acceptance[:,86]==511]

anti_part=tot_dataset_filtered[tot_dataset_filtered[:,86]==-511]
anti_acc=filtered_acceptance[filtered_acceptance[:,86]==-511]

acq_params=pd.read_csv("data/params/acq_params.csv",delimiter=',',dtype='int')
SM_guesses=pd.read_csv("data/params/SM_guesses.csv",delimiter=',',dtype='float32')
acq_params=np.array(acq_params)
SM_guesses=np.array(SM_guesses)

for i in range(0,10):
    
    params=acq_params[i,:]
    guess=SM_guesses[:,i]
    
    sm_fit_func=acceptance_legendre_new(acc, q2_bins, order_costhetal=params[0], order_costhetak=params[1], order_phi=params[3])
    print('done')
    SM_fits_part=sm_fit_func.fit_SM_observables_integral(part, i, guess, intervals=params[3])

    anti_sm_fit_func=acceptance_legendre_new(anti_acc, q2_bins, order_costhetal=params[0], order_costhetak=params[1], order_phi=params[3])
    anti_SM_fits=anti_sm_fit_func.fit_SM_observables_integral(anti_part, i, guess, intervals=params[3])
    print(f'bin {i} finished')
    SM_fits_both=[SM_fits_part,anti_SM_fits]
    
    np.savetxt(f'data/CP_test/bin_{i}.csv',SM_fits_both,delimiter=',')
    


'''


