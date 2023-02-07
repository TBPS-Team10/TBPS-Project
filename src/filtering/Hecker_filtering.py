# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 18:21:21 2023

@author: Utilisateur
"""

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
#%%

def B_meson_filter_conditions(df):
    
    f_d=df
    f_d=f_d.drop(f_d[f_d['B0_IPCHI2_OWNPV']>16].index)
    f_d=f_d.drop(f_d[(f_d['B0_M']>7100)&(f_d['B0_M']<4800)].index)
    f_d=f_d.drop(f_d[np.arccos(f_d['B0_DIRA_OWNPV'])>14e-3].index)
    f_d=f_d.drop(f_d[f_d['B0_FDCHI2_OWNPV']<121].index)
    f_d=f_d.drop(f_d[f_d['B0_ENDVERTEX_CHI2']>8].index)
    
    return f_d

def muon_filter_conditions(df):
    f_d=df
    f_d=f_d.drop(f_d[f_d['J_psi_M']>7100].index)
    f_d=f_d.drop(f_d[f_d['J_psi_ENDVERTEX_CHI2']>9].index)
    
    return f_d

def K_star_filter_conditions(df):
    f_d=df
    f_d=f_d.drop(f_d[f_d['Kstar_M']>6200].index)
    f_d=f_d.drop(f_d[f_d['Kstar_ENDVERTEX_CHI2']>9].index)
    f_d=f_d.drop(f_d[f_d['Kstar_FDCHI2_OWNPV']<9].index)
    
    return f_d
    
def combined_filters(df):
    f_d=df
    f_d=B_meson_filter_conditions(f_d)
    f_d=muon_filter_conditions(f_d)
    f_d=K_star_filter_conditions(f_d)
    
    return f_d

#%% signal dataset
if __name__ == "__main__":
    data_sig=pd.read_csv('../data/sig.csv',delimiter=',')

    B_filtered_data=B_meson_filter_conditions(data_sig)
    mu_filtered_data=muon_filter_conditions(data_sig)
    K_filtered_data=K_star_filter_conditions(data_sig)
    total_filtered_data=combined_filters(data_sig)

    plt.subplot(2,2,1)
    plt.hist(data_sig['q2'],alpha=0.8,color='blue',label='unfiltered data',bins=50)
    plt.hist(B_filtered_data['q2'],alpha=0.5,color='red',label='filtered data',bins=50)
    plt.legend()
    plt.xlabel(r'$q^2$')
    plt.ylabel('frequency')
    plt.title('B filtering conditions')

    plt.subplot(2,2,2)
    plt.hist(data_sig['q2'],alpha=0.8,color='blue',label='unfiltered data',bins=50)
    plt.hist(mu_filtered_data['q2'],alpha=0.5,color='red',label='filtered data',bins=50)
    plt.legend()
    plt.xlabel(r'$q^2$')
    plt.ylabel('frequency')
    plt.title('Muon filtering conditions')

    plt.subplot(2,2,3)
    plt.hist(data_sig['q2'],alpha=0.8,color='blue',label='unfiltered data',bins=50)
    plt.hist(K_filtered_data['q2'],alpha=0.5,color='red',label='filtered data',bins=50)
    plt.legend()
    plt.xlabel(r'$q^2$')
    plt.ylabel('frequency')
    plt.title(r'$K^{*}$ filtering conditions')

    plt.subplot(2,2,4)
    plt.hist(data_sig['q2'],alpha=0.8,color='blue',label='unfiltered data',bins=50)
    plt.hist(total_filtered_data['q2'],alpha=0.5,color='red',label='filtered data',bins=50)
    plt.legend()
    plt.xlabel(r'$q^2$')
    plt.ylabel('frequency')
    plt.title(r'All filtering conditions')

    plt.suptitle(r'Hecker filtering conditions on simulated signal dataset',fontweight='bold')

    plt.show()

    print(len(data_sig.axes[0]))
    print(len(B_filtered_data.axes[0]))
    print(len(mu_filtered_data.axes[0]))
    print(len(K_filtered_data.axes[0]))
    print(len(total_filtered_data.axes[0]))

    #%% total dataset

    data_tot=pd.read_csv('../data/total_dataset.csv',delimiter=',')
    bins=200
    B_filtered_data=B_meson_filter_conditions(data_tot)
    mu_filtered_data=muon_filter_conditions(data_tot)
    K_filtered_data=K_star_filter_conditions(data_tot)
    total_filtered_data=combined_filters(data_tot)

    plt.subplot(2,2,1)
    plt.hist(data_tot['q2'],alpha=0.8,color='blue',label='unfiltered data',bins=bins)
    plt.hist(B_filtered_data['q2'],alpha=0.5,color='red',label='filtered data',bins=bins)
    plt.legend()
    plt.xlabel(r'$q^2$')
    plt.ylabel('frequency')
    plt.title('B filtering conditions')

    plt.subplot(2,2,2)
    plt.hist(data_tot['q2'],alpha=0.8,color='blue',label='unfiltered data',bins=bins)
    plt.hist(mu_filtered_data['q2'],alpha=0.5,color='red',label='filtered data',bins=bins)
    plt.legend()
    plt.xlabel(r'$q^2$')
    plt.ylabel('frequency')
    plt.title('Muon filtering conditions')

    plt.subplot(2,2,3)
    plt.hist(data_tot['q2'],alpha=0.8,color='blue',label='unfiltered data',bins=bins)
    plt.hist(K_filtered_data['q2'],alpha=0.5,color='red',label='filtered data',bins=bins)
    plt.legend()
    plt.xlabel(r'$q^2$')
    plt.ylabel('frequency')
    plt.title(r'$K^{*}$ filtering conditions')

    plt.subplot(2,2,4)
    plt.hist(data_tot['q2'],alpha=0.8,color='blue',label='unfiltered data',bins=bins)
    plt.hist(total_filtered_data['q2'],alpha=0.5,color='red',label='filtered data',bins=bins)
    plt.legend()
    plt.xlabel(r'$q^2$')
    plt.ylabel('frequency')
    plt.title(r'All filtering conditions')

    plt.suptitle(r'Hecker filtering conditions on total dataset dataset',fontweight='bold')

    plt.show()

    print(len(data_tot.axes[0]))
    print(len(B_filtered_data.axes[0]))
    print(len(mu_filtered_data.axes[0]))
    print(len(K_filtered_data.axes[0]))
    print(len(total_filtered_data.axes[0]))


    #%% comparison with ML model
    ML_indices_to_remove=np.where(test_tot_data!=0)[0]
    ML_filtered=data_tot.drop(index=ML_indices_to_remove)
    bins=200

    plt.subplot(2,2,1)
    plt.hist(data_tot['q2'],alpha=0.6,color='blue',label='unfiltered data',bins=bins)
    plt.hist(ML_filtered['q2'],alpha=1,color='green',label='filtered data',bins=bins)
    plt.legend()
    plt.xlabel(r'$q^2$')
    plt.ylabel('frequency')
    plt.title('Machine learning filtering conditions')

    plt.subplot(2,2,2)
    plt.hist(data_tot['q2'],alpha=0.8,color='blue',label='unfiltered data',bins=bins)
    plt.hist(total_filtered_data['q2'],alpha=0.5,color='orange',label='filtered data',bins=bins)
    plt.legend()
    plt.xlabel(r'$q^2$')
    plt.ylabel('frequency')
    plt.title('total Hecker filtering conditions')

    plt.subplot(2,2,3)
    plt.hist(ML_filtered['q2'],alpha=0.6,color='green',label='ML filtered data',bins=bins)
    plt.hist(total_filtered_data['q2'],alpha=1,color='orange',label='Hecker filtered data',bins=bins)
    plt.legend()
    plt.xlabel(r'$q^2$')
    plt.ylabel('frequency')
    plt.title('Machine learning vs Hecker filtering conditions')

    plt.suptitle(r'Hecker filtering vs Machine learning filtering on total dataset',fontweight='bold')

    plt.show()

    print(len(data_tot.axes[0]))
    print(len(ML_filtered.axes[0]))
    print(len(total_filtered_data.axes[0]))
    #%%
    plt.hist(data_tot['q2'],alpha=0.5,color='blue',label='total data',bins=bins)
    plt.hist(total_filtered_data['q2'],alpha=0.8,color='red',label='Hecker filtered data',bins=bins)
    plt.legend()
    plt.xlabel(r'$q^2$')
    plt.ylabel('frequency')
    plt.title('Hecker vs total filtering conditions',fontweight='bold')
    plt.show()

    #%%
    plt.hist(ML_filtered['q2'],alpha=1,color='green',label='ML filtered data',bins=bins,density=False)
    plt.hist(total_filtered_data['q2'],alpha=0.3,color='orange',label='Hecker filtered data',bins=bins,density=False)
    plt.legend()
    plt.xlabel(r'$q^2$')
    plt.ylabel('frequency')
    plt.title('Machine learning vs Hecker filtering conditions',fontweight='bold')
    plt.show()




