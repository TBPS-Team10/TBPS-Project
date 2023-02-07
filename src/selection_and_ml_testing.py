#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 14:21:02 2023

@author: aisulu
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from ml.model_XGB import BDT_model
import filtering.Selection_criteria_func
from scipy.optimize import curve_fit
#%%
variables = pd.read_csv('../data/total_dataset.csv')
variables = list(variables.columns)

bdt_model = BDT_model()
bdt_model.load_model('model_depth_3_estimators_200_features_20.json')
bdt_model.specify_feature_num(20)
feature_list = np.loadtxt('30_features.txt', delimiter = ',', dtype = 'int32')
bdt_model.specify_features(feature_list)
total_dataset = np.loadtxt('../data/total_dataset.csv', delimiter = ',', skiprows = 1)
signal = np.loadtxt('data/sig.csv', delimiter = ',', skiprows = 1)
#%%
test_sig = bdt_model.predict(signal)
plt.hist(test_sig)
plt.title ('test_sig')
#%%
test_total_dataset = bdt_model.predict(total_dataset)
plt.hist(test_total_dataset)
plt.title ('test_total_dataset')
#%%
indices = []
for i in range (len(test_total_dataset)):
    if test_total_dataset[i] != 0:
        indices.append(i)
clean_total_dataset_ML = np.delete(total_dataset, (indices), axis = 0  )
#%%
plt.hist(clean_total_dataset_ML [:,56], bins = 100)
plt.title ('Clean total dataset (ML)')
#%%
df_total = pd.DataFrame(clean_total_dataset_ML, columns = variables)
select(df_total)
plt.hist(df_total['B0_M'], bins = 100)
#%%
plt.hist(clean_total_dataset_ML [:,56], bins = np.linspace(5170,5700,50), density=True, histtype='step', alpha = 0.5,label='after ML')
plt.hist(df_total['B0_M'], bins = np.linspace(5170,5700,50), density=True, histtype='step', alpha = 0.5,label='after ML + filter')
plt.hist(pd.read_csv('../data/total_dataset.csv')['B0_M'], bins = np.linspace(5170,5700,50), density=True, histtype='step', alpha = 0.5,label='Total dataset')

plt.legend()
#%%
total = df_total.to_numpy()
def exp(x, tau, amplitude, mean):
    return amplitude * np.exp(-tau*(x-mean))
def gaussian(x, mean, amplitude, standard_deviation):
    gaus = amplitude * np.exp( - (x - mean)**2 / (2*standard_deviation ** 2))
    return gaus 
def background (popt1, mass):
    x = np.linspace(np.min(mass),np.max(mass),10000)
    y = exp (x, popt1[3], popt1[4], popt1[0])
    #plt.plot(x, y, color = '#539ecd', alpha = 0.5)
    plt.fill_between(x, y, 0, color='#539ecd', label = 'Background', alpha = 0.5)
def signal (popt1, mass):
    x = np.linspace(np.min(mass),np.max(mass),10000)
    y = gaussian (x, popt1[0], popt1[1], popt1[2])
    plt.plot(x, y, color = 'red', alpha = 0.5)
    plt.fill_between(x, y, 0, color='red', label = 'Signal', alpha = 0.5)

def model (x, mean, amplitude, standard_deviation, tau, amplitude2):
    gaus = gaussian(x, mean, amplitude, standard_deviation)
    e = exp(x, tau, amplitude2, mean)
    return gaus + e

def plot_mass_dist (filtered_data, q2_bin):
    q2_bins = [[0.1, 0.98], [1.1, 2.5], [2.5, 4.0], [4.0, 6.0], [6.0, 8.0], 
               [15.0, 17.0], [17.0, 19.0], [11.0, 12.5], [1.0, 6.0], [15.0, 19.0]]
    q = filtered_data[q2_bins[q2_bin][0] < filtered_data[:,90]]
    q = q[q[:,90] < q2_bins[q2_bin][1]]
    mass = q[:,56]
    bin_heights1, bin_borders1, _ = plt.hist(mass, bins= 50, rwidth = 0)
    bin_centers1 = bin_borders1[:-1] + np.diff(bin_borders1) / 2
    popt1, pcov1 = curve_fit(model, bin_centers1, bin_heights1, p0=[5280, 25, 14, 4.6e-4, 0.6])
    mass_interval_for_fit = np.linspace(bin_borders1[0], bin_borders1[-1], 10000)
    background(popt1, mass)
    signal(popt1, mass)
    plt.plot(mass_interval_for_fit, model(mass_interval_for_fit, *popt1), label='fit', color = 'grey')
    yerr = np.sqrt(bin_heights1)
    xerr=(bin_borders1[1] - bin_borders1[0])/2
    plt.errorbar(bin_centers1, bin_heights1, yerr = yerr,xerr = xerr, fmt = '.', c = 'black', label = 'ML + selection Filtered data')
    plt.legend()
    plt.xlim ([np.min(mass), np.max(mass)])
    plt.title ('q2 bin: %i' %q2_bin )
    plt.xlabel ('B0_M')
    plt.ylabel('Events')
    
plot_mass_dist (total, 8)
      
















