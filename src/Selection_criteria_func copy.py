#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 13:15:49 2023

@author: aisulu
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from iminuit import Minuit
import mpl_scatter_density # adds projection='scatter_density'
from matplotlib.colors import LinearSegmentedColormap
#%%
#Deleting certain ranges in q2
#Literature values are not used
#Values for conditions are taken by observing B0_M vs q2 and finding these regions 
def cut_q2 (df):
    df.drop(df[(df['q2'] > 9.297)&(df['q2']< 9.898)&(df['B0_M'] > 5225.7)&(df['B0_M'] < 5339)].index, inplace=True)
    df.drop(df[(df['q2'] > 8.557)&(df['q2']< 9.357)&(df['B0_M'] > 5175.7)&(df['B0_M'] < 5260.4)].index, inplace=True)
    df.drop(df[(df['q2'] > 9)&(df['q2']<10.0)].index, inplace=True)
    df.drop(df[(df['q2'] > 8.431)&(df['q2']< 9.037)&(df['B0_M'] > 5170)&(df['B0_M'] < 5177)].index, inplace=True)
    df.drop(df[(df['q2'] > 12.517)&(df['q2']<14.266)&(df['B0_M'] > 5170)&(df['B0_M'] < 5368)].index, inplace=True)
    df.drop(df[(df['q2'] > 13.27)&(df['q2']<14.58)].index, inplace=True)
    df.drop(df[(df['q2'] > 8.0)&(df['q2']<11.0)].index, inplace=True)
    df.drop(df[(df['q2'] > 12.5)&(df['q2']<15.0)].index, inplace=True)
    df.drop(df[(df['q2'] > 0.98)&(df['q2']<1.10)].index, inplace=True)
    
#Deleting certain ranges in B0
#Threshold values are taken by stat analysis and 3 sigma significance
def cut_B0_M (df):
    mean = np.mean(df['B0_M'])
    sigma = np.std(df['B0_M'])
    lower_range = mean-(3*sigma)
    upper_range = mean+(3*sigma)
    df.drop(df[(df['B0_M'] < lower_range)].index, inplace=True)
    df.drop(df[(df['B0_M'] > upper_range)].index, inplace=True)

#Deleting regions in IP chi squared
# "B0" is the value for B0_IPCHI2_OWNPV
# "other" is the value for IPCHI_OWNPV for mu, K, and Pi
def cut_IP_chisq (df, B0=16, other=6.05):
    df.drop(df[(df['mu_plus_IPCHI2_OWNPV'] <= other)].index, inplace=True)
    df.drop(df[(df['mu_minus_IPCHI2_OWNPV'] <= other)].index, inplace=True)
    df.drop(df[(df['K_IPCHI2_OWNPV'] <= other)].index, inplace=True)
    df.drop(df[(df['Pi_IPCHI2_OWNPV'] <= other)].index, inplace=True)
    df.drop(df[(df['B0_IPCHI2_OWNPV'] >= B0)].index, inplace=True)
    
#Deleting regions in mass of Kstar
#Values not taken from literature
#2 sigma significance
def cut_K_mass(df):
    mean = np.mean(df['Kstar_M'])
    sigma = np.std(df['Kstar_M'])
    lower_range = mean-(2*sigma)
    upper_range = mean+(2*sigma)
    df.drop(df[(df['Kstar_M'] < lower_range)].index, inplace=True)
    df.drop(df[(df['Kstar_M'] > upper_range)].index, inplace=True)

#Values not taken from literature
def cut_sep_vertex(df):
    df.drop(df[(df['B0_FDCHI2_OWNPV'] < 64)].index, inplace=True)
    df.drop(df[(df['Kstar_FDCHI2_OWNPV'] < 16)].index, inplace=True)
    
#Deleting regions in DIRA
#Values not taken from literature
def cut_dira(df):
    df.drop(df[(df['B0_DIRA_OWNPV'] < 0.99990)].index, inplace=True)
        
#Deleting regions where the seperation angle between 2 partciles is less than 0.001
#Values taken from literature
def cut_small_theta_sep (df):
    df.drop(df[(df['mu_plus_ETA']-df['mu_minus_ETA'] < 0.001)&(df['mu_plus_ETA']-df['mu_minus_ETA'] > -0.001)].index, inplace=True)
    df.drop(df[(df['mu_plus_ETA']-df['K_ETA'] < 0.001)&(df['mu_plus_ETA']-df['K_ETA'] > -0.001)].index, inplace=True)
    df.drop(df[(df['mu_plus_ETA']-df['Pi_ETA'] < 0.001)&(df['mu_plus_ETA']-df['Pi_ETA'] > -0.001)].index, inplace=True)
    df.drop(df[(df['mu_minus_ETA']-df['K_ETA'] < 0.001)&(df['mu_minus_ETA']-df['K_ETA'] > -0.001)].index, inplace=True)
    df.drop(df[(df['mu_minus_ETA']-df['Pi_ETA'] < 0.001)&(df['mu_minus_ETA']-df['Pi_ETA'] > -0.001)].index, inplace=True)
    df.drop(df[(df['K_ETA']-df['Pi_ETA'] < 0.001)&(df['K_ETA']-df['Pi_ETA'] > -0.001)].index, inplace=True)

    
def cut_prob(df):
    df.drop(df[(df['Pi_ProbNNpi'] < 0.2)].index, inplace=True)
    df.drop(df[(df['K_ProbNNk'] < 0.5)].index, inplace=True)
    df.drop(df[(df['mu_minus_ProbNNmu'] < 0.8)].index, inplace=True)
    df.drop(df[(df['mu_plus_ProbNNmu'] < 0.8)].index, inplace=True)
    
#Deleting misundentified pi
def cut_pik(df):
    df.drop(df[(df['Pi_ProbNNp']-df['Pi_ProbNNpi'] > 0.00)&(df['B0_M'] > 5170)&(df['B0_M'] < 5691)].index, inplace = True)
    df.drop(df[(df['Pi_ProbNNk']-df['Pi_ProbNNpi'] > 0.00)&(df['B0_M'] > 5170)&(df['B0_M'] < 5691)].index, inplace = True)
    
#Deleting Jpsi
def cut_jpsi(df):
    df.drop(df[(df['Pi_ProbNNmu'] > 0.6)&(df['J_psi_M'] > 540)&(df['J_psi_M'] < 3500)].index, inplace = True)
    df.drop(df[(df['Pi_ProbNNpi'] < 0.2)&(df['J_psi_M'] > 540)&(df['J_psi_M'] < 3500)].index, inplace = True)
    df.drop(df[(df['K_ProbNNk'] < 0.2)&(df['J_psi_M'] > 420)&(df['J_psi_M'] < 4100)].index, inplace = True)
    df.drop(df[(df['K_ProbNNmu'] > 0.6)&(df['J_psi_M'] > 420)&(df['J_psi_M'] < 4100)].index, inplace = True)
    
#Deleting phimumu
def cut_phimumu(df):
    df.drop(df[(df['Pi_ProbNNpi'] -df['Pi_ProbNNk'] < 0.75)&(df['Kstar_M'] > 745)&(df['Kstar_M'] < 1095)
              &(df['B0_M'] > 5170)&(df['B0_M'] < 5698)].index, inplace = True)

#Deleting k pi swap
def cut_kpi(df):
    df.drop(df[(df['Pi_ProbNNpi']-df['Pi_ProbNNk'] < 0.75)].index, inplace = True)
    df.drop(df[(df['K_ProbNNk']-df['K_ProbNNpi'] < 0.75)].index, inplace = True)
    
#Cutting momentum 2 sigma significance
def cut_momX(df):
    mean = np.mean(df['B0_PX'])
    sigma = np.std(df['B0_PX'])
    lower_range = mean-(2*sigma)
    upper_range = mean+(2*sigma)
    df.drop(df[(df['mu_minus_PX']+df['mu_plus_PX']+df['Pi_PX']+df['K_PX'] < lower_range)].index, inplace=True)
    df.drop(df[(df['mu_minus_PX']+df['mu_plus_PX']+df['Pi_PX']+df['K_PX'] > upper_range)].index, inplace=True)
    
def cut_momY(df):
    mean = np.mean(df['B0_PY'])
    sigma = np.std(df['B0_PY'])
    lower_range = mean-(2*sigma)
    upper_range = mean+(2*sigma)
    df.drop(df[(df['mu_minus_PY']+df['mu_plus_PY']+df['Pi_PY']+df['K_PY'] < lower_range)].index, inplace=True)
    df.drop(df[(df['mu_minus_PY']+df['mu_plus_PY']+df['Pi_PY']+df['K_PY'] > upper_range)].index, inplace=True)
    
def cut_momZ(df):
    mean = np.mean(df['B0_PZ'])
    sigma = np.std(df['B0_PZ'])
    lower_range = mean-(2*sigma)
    upper_range = mean+(2*sigma)
    df.drop(df[(df['mu_minus_PZ']+df['mu_plus_PZ']+df['Pi_PZ']+df['K_PZ'] < lower_range)].index, inplace=True)
    df.drop(df[(df['mu_minus_PZ']+df['mu_plus_PZ']+df['Pi_PZ']+df['K_PZ'] > upper_range)].index, inplace=True)
    
def cut_mom(df):
    cut_momX(df)
    cut_momY(df)
    cut_momZ(df)

po = [403.67914507, 896.71732264,  26.35192252]

def cut_Kmumu(df):
    mean = po[1]
    sigma = po[2]
    lower_range = mean-(3*sigma)
    upper_range = mean+(3*sigma)
    df.drop(df[(df['Kstar_M'] < lower_range)].index, inplace=True)
    df.drop(df[(df['Kstar_M'] > upper_range)].index, inplace=True)

    
#Combining all filtering functions above 
def select(df):
    cut_small_theta_sep(df)
    cut_q2(df)
    cut_B0_M(df)
    cut_IP_chisq(df)
    cut_K_mass(df)
    cut_pik(df)
    cut_jpsi(df)
    cut_phimumu(df)
    cut_kpi(df)
    cut_sep_vertex(df)
    cut_mom(df)
    cut_dira(df)
    cut_prob(df)
    cut_Kmumu(df)