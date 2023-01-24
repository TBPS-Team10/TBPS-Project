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

def cut_q2 (df):
    df.drop(df[(df['q2'] > 8.0)&(df['q2']<11.0)].index, inplace=True)
    df.drop(df[(df['q2'] > 12.5)&(df['q2']<15.0)].index, inplace=True)
    df.drop(df[(df['q2'] > 0.98)&(df['q2']<1.10)].index, inplace=True)
    
def cut_B0_M (df):
    df.drop(df[(df['B0_M'] < 4850)].index, inplace=True)
    df.drop(df[(df['B0_M'] > 5780)].index, inplace=True)

def cut_IP_chisq (df):
    df.drop(df[(df['mu_plus_IPCHI2_OWNPV'] <= 9)].index, inplace=True)
    df.drop(df[(df['mu_minus_IPCHI2_OWNPV'] <= 9)].index, inplace=True)
    df.drop(df[(df['K_IPCHI2_OWNPV'] <= 9)].index, inplace=True)
    df.drop(df[(df['Pi_IPCHI2_OWNPV'] <= 9)].index, inplace=True)
    df.drop(df[(df['B0_IPCHI2_OWNPV'] >= 16)].index, inplace=True)
    
def cut_K_mass(df):
    df.drop(df[(df['Kstar_M'] < 792)].index, inplace=True)
    df.drop(df[(df['Kstar_M'] > 922)].index, inplace=True)
    
def cut_sep_vertex(df):
    df.drop(df[(df['B0_FDCHI2_OWNPV'] < 121)].index, inplace=True)
    df.drop(df[(df['Kstar_FDCHI2_OWNPV'] < 9)].index, inplace=True)
    
def cut_dira(df):
    df.drop(df[(df['B0_DIRA_OWNPV'] < 0.9999)].index, inplace=True)
    
def cut_false_particles(df):
    #Choose prob to be > 90%
    df.drop(df[(df['mu_plus_ProbNNmu'] < 0.90)].index, inplace=True)
    df.drop(df[(df['mu_minus_ProbNNmu'] < 0.90)].index, inplace=True)
    #df.drop(df[(df['K_ProbNNk'] < 0.90)].index, inplace=True)
    #df.drop(df[(df['Pi_ProbNNpi'] < 0.90)].index, inplace=True)
    
def cut_small_theta_sep (df):
    theta1 = np.array(df['mu_plus_ETA'].tolist()) - np.array(df['mu_minus_ETA'].tolist()) 
    theta2 = np.array(df['mu_plus_ETA'].tolist()) - np.array(df['K_ETA'].tolist()) 
    theta3 = np.array(df['mu_plus_ETA'].tolist()) - np.array(df['Pi_ETA'].tolist())
    theta4 = np.array(df['mu_minus_ETA'].tolist()) - np.array(df['K_ETA'].tolist())
    theta5 = np.array(df['mu_minus_ETA'].tolist()) - np.array(df['Pi_ETA'].tolist())
    theta6 = np.array(df['K_ETA'].tolist()) - df['Pi_ETA'].tolist()
    for i in range (len(theta1)):
        if theta1[i] < 0.001 and theta1[i]> -0.001:
            df = df.drop(i)
        elif theta2[i] < 0.001 and theta2[i]> -0.001:
            df = df.drop(i)
        elif theta3[i] < 0.001 and theta3[i]> -0.001:
            df = df.drop(i)
        elif theta4[i] < 0.001 and theta4[i]> -0.001:
            df = df.drop(i)
        elif theta5[i] < 0.001 and theta5[i]> -0.001:
            df = df.drop(i)
        elif theta6[i] < 0.001 and theta6[i]> -0.001:
            df = df.drop(i)

def select(df):
    cut_small_theta_sep(df)
    cut_q2(df)
    cut_B0_M(df)
    cut_IP_chisq(df)
    cut_K_mass(df)
    cut_sep_vertex(df)
    cut_dira(df)
    cut_false_particles(df)
   
#%%
dataset = pd.read_csv('data/total_dataset.csv')
print (dataset)
#%%
select(dataset)

x = dataset['B0_M'] 
y = dataset['q2']

white_viridis = LinearSegmentedColormap.from_list('white_viridis', [
    (0, '#ffffff'),
    (1e-20, '#440053'),
    (0.2, '#404388'),
    (0.4, '#2a788e'),
    (0.6, '#21a784'),
    (0.8, '#78d151'),
    (1, '#fde624'),
], N=len(y))

def using_mpl_scatter_density(fig, x, y):
    ax = fig.add_subplot(1, 1, 1, projection='scatter_density')
    density = ax.scatter_density(x, y, cmap=white_viridis)
    fig.colorbar(density, label='Number of points per pixel')

fig = plt.figure()
using_mpl_scatter_density(fig, x, y)
plt.ylabel ('q2')
plt.xlabel ('B0_M')
plt.title ('Filtered dataset')
plt.show()
#%%
edg = []

vals, edges = np.histogram(x, bins=100)
for i in range (len (vals)):
    edg.append(0.5*(edges[i]+edges[i+1]))

plt.plot (edg, vals , '.')
plt.xlabel('B0_M')
plt.ylabel('Freq')
plt.title ('"Filtered" total dataset')

