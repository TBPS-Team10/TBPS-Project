# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from iminuit import Minuit
import mpl_scatter_density # adds projection='scatter_density'
from matplotlib.colors import LinearSegmentedColormap
import os

my_path = os.path.abspath('/Users/aisulu/Desktop/TBPS/TBPS/plots')
#%%
df_sig = pd.read_csv('data/sig.csv')
df_dataset = pd.read_csv('data/total_dataset.csv')
df_jpsi_kstarp_pi0 = pd.read_csv ('data/Jpsi_Kstarp_pi0.csv')
df_jpsi_mu_k_swap = pd.read_csv ('data/jpsi_mu_k_swap.csv')
df_jpsi_mu_pi_swap = pd.read_csv ('data/jpsi_mu_pi_swap.csv')
df_jpsi = pd.read_csv ('data/jpsi.csv')
df_k_pi_swap = pd.read_csv ('data/k_pi_swap.csv')
df_Kmumu = pd.read_csv ('data/Kmumu.csv')
df_Kstarp_pi0 = pd.read_csv ('data/Kstarp_pi0.csv')
df_phimumu = pd.read_csv ('data/phimumu.csv')
df_pKmumu_piTok_kTop = pd.read_csv ('data/pKmumu_piTok_kTop.csv')
df_pKmumu_piTop = pd.read_csv ('data/pKmumu_piTop.csv')
df_psi2S = pd.read_csv ('data/psi2S.csv')
#%%
x = df_sig['B0_M'] 
y = df_sig['q2']

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
plt.title ('sig.csv')
my_file = 'B0_vs_q2_sig.png'
plt.savefig(os.path.join(my_path, my_file))
plt.show()

#%%
x = df_jpsi_kstarp_pi0['B0_M'] 
y = df_jpsi_kstarp_pi0['q2']

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
plt.title ('jpsi_kstarp_pi0.csv')
my_file = 'B0_vs_q2_jpsi_kstarp_pi0.png'
plt.savefig(os.path.join(my_path, my_file))
plt.show()
#%%
x = df_jpsi_mu_k_swap['B0_M'] 
y = df_jpsi_mu_k_swap['q2']

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
plt.title ('jpsi_mu_k_swap.csv')
my_file = 'B0_vs_q2_jpsi_mu_k_swap.png'
plt.savefig(os.path.join(my_path, my_file))
plt.show()
#%%
x = df_jpsi_mu_pi_swap['B0_M'] 
y = df_jpsi_mu_pi_swap['q2']

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
plt.title ('jpsi_mu_pi_swap.csv')
my_file = 'B0_vs_q2_jpsi_mu_pi_swap.png'
plt.savefig(os.path.join(my_path, my_file))
plt.show()
#%%
x = df_jpsi['B0_M'] 
y = df_jpsi['q2']

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
plt.title ('jpsi.csv')
my_file = 'B0_vs_q2_jpsi.png'
plt.savefig(os.path.join(my_path, my_file))
plt.show()
#%%
x = df_k_pi_swap['B0_M'] 
y = df_k_pi_swap['q2']

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
plt.title ('k_pi_swap.csv')
my_file = 'B0_vs_q2_k_pi_swap.png'
plt.savefig(os.path.join(my_path, my_file))
plt.show()
#%%
x = df_Kmumu['B0_M'] 
y = df_Kmumu['q2']

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
plt.title ('Kmumu.csv')
my_file = 'B0_vs_q2_Kmumu.png'
plt.savefig(os.path.join(my_path, my_file))
plt.show()
#%%
x = df_Kstarp_pi0['B0_M'] 
y = df_Kstarp_pi0['q2']

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
plt.title ('Kstarp_pi0.csv')
my_file = 'B0_vs_q2_Kstarp_pi0.png'
plt.savefig(os.path.join(my_path, my_file))
plt.show()
#%%
x = df_phimumu['B0_M'] 
y = df_phimumu['q2']

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
plt.title ('phimumu.csv')
my_file = 'B0_vs_q2_phimumu.png'
plt.savefig(os.path.join(my_path, my_file))
plt.show()
#%%
x = df_pKmumu_piTok_kTop['B0_M'] 
y = df_pKmumu_piTok_kTop['q2']

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
plt.title ('pKmumu_piTok_kTop.csv')
my_file = 'B0_vs_q2_pKmumu_piTok_kTop.png'
plt.savefig(os.path.join(my_path, my_file))
plt.show()
#%%
x = df_pKmumu_piTop['B0_M'] 
y = df_pKmumu_piTop['q2']

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
plt.title ('pKmumu_piTop.csv')
my_file = 'B0_vs_q2_pKmumu_piTop.png'
plt.savefig(os.path.join(my_path, my_file))
plt.show()
#%%
x = df_psi2S['B0_M'] 
y = df_psi2S['q2']

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
plt.title ('psi2S.csv')
my_file = 'B0_vs_q2_psi2S.png'
plt.savefig(os.path.join(my_path, my_file))
plt.show()
#%%
x = df_dataset['B0_M'] 
y = df_dataset['q2']

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
plt.title ('total_dataset.csv')
my_file = 'B0_vs_q2_total_dataset.png'
plt.savefig(os.path.join(my_path, my_file))
plt.show()
#%%
df = pd.read_csv('data/total_dataset.csv')

df.drop(df[(df['q2'] > 8.0)&(df['q2']<11.0)].index, inplace=True)
df.drop(df[(df['q2'] > 12.5)&(df['q2']<15.0)].index, inplace=True)
df.drop(df[(df['q2'] > 0.98)&(df['q2']<1.10)].index, inplace=True)
df.drop(df[(df['B0_M'] < 5170)].index, inplace=True)
df.drop(df[(df['B0_M'] > 5700)].index, inplace=True)

x = df['B0_M']
y = df['q2']

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
plt.title ('total_dataset.csv')
my_file = 'B0_vs_q2_total_dataset_filtered.png'
plt.savefig(os.path.join(my_path, my_file))
plt.show()

#%%
df.drop(df[(df['q2'] > 8.0)].index, inplace=True)
df.drop(df[(df['q2'] < 5.0)].index, inplace=True)  

x = df['B0_M']             

vals, edges = np.histogram(x, bins=100)


plt.plot (x, vals , '.')
plt.xlabel('B0_M')
plt.ylabel('Freq')
plt.title ('"Filtered" total dataset')
#my_file = 'B0_vs_q2_total_dataset_filtered_hist.png'
#plt.savefig(os.path.join(my_path, my_file))

    
