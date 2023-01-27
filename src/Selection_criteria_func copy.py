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
#Normalizing ProbNN
def normalize(probs):
    prob_factor = 1 / sum(probs)
    return [prob_factor * p for p in probs]

def normalize_df(df, row):
    prob_mu_minus = [ df.loc[row, 'mu_minus_ProbNNk'], 
                          df.loc[row, 'mu_minus_ProbNNpi'], 
                          df.loc[row, 'mu_minus_ProbNNmu'],
                          df.loc[row, 'mu_minus_ProbNNe'],
                          df.loc[row, 'mu_minus_ProbNNp']]
    prob_mu_minus = normalize(prob_mu_minus)
    df.loc[row, 'mu_minus_ProbNNk' ] = prob_mu_minus[0]
    df.loc[row, 'mu_minus_ProbNNpi' ] = prob_mu_minus[1]
    df.loc[row, 'mu_minus_ProbNNmu' ] = prob_mu_minus[2]
    df.loc[row, 'mu_minus_ProbNNe' ] = prob_mu_minus[3]
    df.loc[row, 'mu_minus_ProbNNp' ] = prob_mu_minus[4]
    
    prob_mu_plus =  [df.loc[row, 'mu_plus_ProbNNk'], 
                          df.loc[row, 'mu_plus_ProbNNpi'], 
                          df.loc[row, 'mu_plus_ProbNNmu'],
                          df.loc[row, 'mu_plus_ProbNNe'],
                          df.loc[row, 'mu_plus_ProbNNp']]
    prob_mu_plus = normalize(prob_mu_plus)
    df.loc[row, 'mu_plus_ProbNNk' ] = prob_mu_plus[0]
    df.loc[row, 'mu_plus_ProbNNpi' ] = prob_mu_plus[1]
    df.loc[row, 'mu_plus_ProbNNmu' ] = prob_mu_plus[2]
    df.loc[row, 'mu_plus_ProbNNe' ] = prob_mu_plus[3]
    df.loc[row, 'mu_plus_ProbNNp' ] = prob_mu_plus[4]
    
    prob_K = [df.loc[row, 'K_ProbNNk'], 
                          df.loc[row, 'K_ProbNNpi'], 
                          df.loc[row, 'K_ProbNNmu'],
                          df.loc[row, 'K_ProbNNe'],
                          df.loc[row, 'K_ProbNNp']]
    prob_K = normalize(prob_K)
    df.loc[row, 'K_ProbNNk' ] = prob_K[0]
    df.loc[row, 'K_ProbNNpi' ] = prob_K[1]
    df.loc[row, 'K_ProbNNmu' ] = prob_K[2]
    df.loc[row, 'K_ProbNNe' ] = prob_K[3]
    df.loc[row, 'K_ProbNNp' ] = prob_K[4]
    
    prob_Pi = [df.loc[row, 'Pi_ProbNNk'], 
                          df.loc[row, 'Pi_ProbNNpi'], 
                          df.loc[row, 'Pi_ProbNNmu'],
                          df.loc[row, 'Pi_ProbNNe'],
                          df.loc[row, 'Pi_ProbNNp']]
    prob_Pi = normalize(prob_Pi)
    df.loc[row, 'Pi_ProbNNk' ] = prob_Pi[0]
    df.loc[row, 'Pi_ProbNNpi' ] = prob_Pi[1]
    df.loc[row, 'Pi_ProbNNmu' ] = prob_Pi[2]
    df.loc[row, 'Pi_ProbNNe' ] = prob_Pi[3]
    df.loc[row, 'Pi_ProbNNp' ] = prob_Pi[4]
    
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
    #df.drop(df[(df['q2'] > 8.0)&(df['q2']<11.0)].index, inplace=True)
    #df.drop(df[(df['q2'] > 12.5)&(df['q2']<15.0)].index, inplace=True)
    #df.drop(df[(df['q2'] > 0.98)&(df['q2']<1.10)].index, inplace=True)
    
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
def cut_IP_chisq (df, B0, other):
    df.drop(df[(df['mu_plus_IPCHI2_OWNPV'] <= other)].index, inplace=True)
    df.drop(df[(df['mu_minus_IPCHI2_OWNPV'] <= other)].index, inplace=True)
    df.drop(df[(df['K_IPCHI2_OWNPV'] <= other)].index, inplace=True)
    df.drop(df[(df['Pi_IPCHI2_OWNPV'] <= other)].index, inplace=True)
    df.drop(df[(df['B0_IPCHI2_OWNPV'] >= B0)].index, inplace=True)
    
#Deleting regions in mass of Kstar
#Values taken from literature
def cut_K_mass(df):
    df.drop(df[(df['Kstar_M'] < 792)].index, inplace=True)
    df.drop(df[(df['Kstar_M'] > 922)].index, inplace=True)
 
#Deleting regions in FDCHI2_OWNPV
#Values taken from literature
def cut_sep_vertex(df):
    df.drop(df[(df['B0_FDCHI2_OWNPV'] < 121)].index, inplace=True)
    df.drop(df[(df['Kstar_FDCHI2_OWNPV'] < 9)].index, inplace=True)
    
#Deleting regions in DIRA
#Values taken from literature
def cut_dira(df):
    df.drop(df[(df['B0_DIRA_OWNPV'] < 0.9999)].index, inplace=True)
        
#Deleting regions where the seperation angle between 2 partciles is less than 0.001
#Values taken from literature
def cut_small_theta_sep (df):
    df.drop(df[(df['mu_plus_ETA']-df['mu_minus_ETA'] < 0.001)&(df['mu_plus_ETA']-df['mu_minus_ETA'] > -0.001)].index, inplace=True)
    df.drop(df[(df['mu_plus_ETA']-df['K_ETA'] < 0.001)&(df['mu_plus_ETA']-df['K_ETA'] > -0.001)].index, inplace=True)
    df.drop(df[(df['mu_plus_ETA']-df['Pi_ETA'] < 0.001)&(df['mu_plus_ETA']-df['Pi_ETA'] > -0.001)].index, inplace=True)
    df.drop(df[(df['mu_minus_ETA']-df['K_ETA'] < 0.001)&(df['mu_minus_ETA']-df['K_ETA'] > -0.001)].index, inplace=True)
    df.drop(df[(df['mu_minus_ETA']-df['Pi_ETA'] < 0.001)&(df['mu_minus_ETA']-df['Pi_ETA'] > -0.001)].index, inplace=True)
    df.drop(df[(df['K_ETA']-df['Pi_ETA'] < 0.001)&(df['K_ETA']-df['Pi_ETA'] > -0.001)].index, inplace=True)

#Combining all filtering functions above 
def select(df):
    cut_small_theta_sep(df)
    cut_q2(df)
    cut_B0_M(df)
    cut_IP_chisq(df, 16, 9)
    cut_K_mass(df)
    cut_sep_vertex(df)
    cut_dira(df)
    #for row in df.index:
        #normalize_df(df, row)