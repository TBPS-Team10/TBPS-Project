#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 16:31:27 2023

@author: aisulu
"""

import matplotlib.pyplot as plt
import numpy as np
import model_XGB
import pandas as pd
import Finalised_filters 
from scipy.optimize import curve_fit
import mpl_scatter_density # adds projection='scatter_density'
from matplotlib.colors import LinearSegmentedColormap
import math
#%%
def plot_filtered_data_gaus(total_dataset_file,signal_file, ML_model_json):
    variables = pd.read_csv(total_dataset_file)
    variables = list(variables.columns)
    
    bdt_model = BDT_model()
    bdt_model.load_model(ML_model_json)
    bdt_model.specify_feature_num(20)
    feature_list = np.loadtxt('30_features.txt', delimiter = ',', dtype = 'int32')
    bdt_model.specify_features(feature_list)
    
    total_dataset = np.loadtxt(total_dataset_file, delimiter = ',', skiprows = 1)
    
    test_total_dataset = bdt_model.predict(total_dataset)
    
    indices = []
    for i in range (len(test_total_dataset)):
        if test_total_dataset[i] != 0:
            indices.append(i)
    clean_total_dataset_ML = np.delete(total_dataset, (indices), axis = 0  )
    
    df_total = pd.DataFrame(clean_total_dataset_ML, columns = variables)
    filter_light(pd.read_csv(signal_file),df_total)
    
    def exp(x, tau, amplitude, mean):
        return amplitude * np.exp(-tau*(x-mean)/mean)
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
                   [15.0, 17.0], [17.0, 19.0], [11.0, 12.5], [1.0, 6.0], [15.0, 19.0], [0.1, 19.0]]
        q = filtered_data[q2_bins[q2_bin][0] < filtered_data[:,90]]
        q = q[q[:,90] < q2_bins[q2_bin][1]]
        mass = q[:,56]
        bin_heights1, bin_borders, _ = plt.hist(mass, bins= 50, rwidth = 0)
        bin_centers1 = bin_borders[:-1] + np.diff(bin_borders) / 2
        popt1, pcov1 = curve_fit(model, bin_centers1, bin_heights1, p0=[5280, 25, 14, 5e-3, 30])
        mass_interval_for_fit = np.linspace(bin_borders[0], bin_borders[-1], 10000)
        background(popt1, mass)
        signal(popt1, mass)
        plt.plot(mass_interval_for_fit, model(mass_interval_for_fit, *popt1), label='fit', color = 'grey')
        yerr = np.sqrt(bin_heights1)
        xerr=(bin_borders[1] - bin_borders[0])/2
        plt.errorbar(bin_centers1, bin_heights1, yerr = yerr,xerr = xerr, fmt = '.', c = 'black', label = 'ML + selection Filtered data')
        #plt.legend()
        plt.xlim ([np.min(mass), np.max(mass)])
        plt.ylim ([1, np.max(bin_heights1)])
        plt.title (r'$q^2$ bin: %i' %q2_bin )
        plt.xlabel (r'$B^0_M$')
        plt.ylabel('Events')
        
    plt.figure(figsize=(10,10))
    plt.subplot(4,3,1)
    plot_mass_dist(df_total.to_numpy(), 0)
    plt.subplot(4,3,2)
    plot_mass_dist(df_total.to_numpy(), 1)
    plt.subplot(4,3,3)
    plot_mass_dist(df_total.to_numpy(), 2)
    plt.subplot(4,3,4)
    plot_mass_dist(df_total.to_numpy(), 3)
    plt.subplot(4,3,5)
    plot_mass_dist(df_total.to_numpy(), 4)
    plt.subplot(4,3,6)
    plot_mass_dist(df_total.to_numpy(), 5)
    plt.subplot(4,3,7)
    plot_mass_dist(df_total.to_numpy(), 6)
    plt.subplot(4,3,8)
    plot_mass_dist(df_total.to_numpy(), 7)
    plt.subplot(4,3,9)
    plot_mass_dist(df_total.to_numpy(), 8)
    plt.subplot(4,3,10)
    plot_mass_dist(df_total.to_numpy(), 9)
    
    plt.tight_layout()
    
plot_filtered_data_gaus('data/total_dataset.csv','data/sig.csv','model_depth_3_estimators_200_features_20.json')
#%%
def plot_filtered_data_crystal(total_dataset_file,signal_file, ML_model_json):
    variables = pd.read_csv(total_dataset_file)
    variables = list(variables.columns)
    
    bdt_model = BDT_model()
    bdt_model.load_model(ML_model_json)
    bdt_model.specify_feature_num(20)
    feature_list = np.loadtxt('30_features.txt', delimiter = ',', dtype = 'int32')
    bdt_model.specify_features(feature_list)
    
    total_dataset = np.loadtxt(total_dataset_file, delimiter = ',', skiprows = 1)
    
    test_total_dataset = bdt_model.predict(total_dataset)
    
    indices = []
    for i in range (len(test_total_dataset)):
        if test_total_dataset[i] != 0:
            indices.append(i)
    clean_total_dataset_ML = np.delete(total_dataset, (indices), axis = 0  )
    
    df_total = pd.DataFrame(clean_total_dataset_ML, columns = variables)
    filter_light(pd.read_csv(signal_file),df_total)
    
    def exp(x, tau, amplitude, mean):
        return amplitude * np.exp(-tau*(x-mean))
    
    def crystal_ball(mass, mean, std, alpha, n):
        A = (n/abs(alpha))**n * np.exp(-0.5*abs(alpha)**2)
        B = n/abs(alpha) - abs(alpha)
        D = np.sqrt(np.pi/2) * (1 + math.erf(abs(alpha) / np.sqrt(2)))
        C = (n/abs(alpha))*(1/(n-1))*(np.exp(-abs(alpha)**2/2)) 
        N = 1 / (std * (C + D))
        x = (mass-mean)/std
    
        return np.piecewise(x, [x > - alpha, x <= -alpha], 
                            [lambda x: N * np.exp(-0.5*(x)**2),
                             lambda x: N * A * ((B - x)**(-n))])
                 
    def signal_model(mass, mean, std1, std2, alpha, n, f, amplitude):
        signal1 = crystal_ball(mass, mean, std1,alpha, n)
        signal2 = crystal_ball(mass, mean, std2,alpha, n)
        return amplitude*(f*signal1 + (1-f)*signal2)

    def model (mass, mean, std1, std2, alpha, n, f, tau, amplitude_exp, amplitude_sig):
        sig = signal_model(mass, mean, std1, std2, alpha, n, f,amplitude_sig)
        bg = exp(mass, tau, amplitude_exp, mean)
        return sig + bg
    
    def signal(mass, popt1):
        x = np.linspace(np.min(mass),np.max(mass),10000)
        y = signal_model (x, popt1[0], popt1[1], popt1[2],popt1[3],popt1[4],popt1[5],popt1[8])
        plt.plot(x, y, color = 'red', alpha = 0.5)
        plt.fill_between(x, y, 0, color='red', label = 'Signal', alpha = 0.5)
    def background (mass, popt1):
        x = np.linspace(np.min(mass),np.max(mass),10000)
        y = exp (x, popt1[6], popt1[7], popt1[0])
        plt.plot(x, y, color = '#539ecd', alpha = 0.5)
        plt.fill_between(x, y, 0, color='#539ecd', label = 'Background', alpha = 0.5)
    def plot_mass_dist (filtered_data, q2_bin):
        q2_bins = [[0.1, 0.98], [1.1, 2.5], [2.5, 4.0], [4.0, 6.0], [6.0, 8.0], 
                   [15.0, 17.0], [17.0, 19.0], [11.0, 12.5], [1.0, 6.0], [15.0, 19.0], [0.1, 19.0]]
        q = filtered_data[q2_bins[q2_bin][0] < filtered_data[:,90]]
        q = q[q[:,90] < q2_bins[q2_bin][1]]
        mass = q[:,56]
        bin_heights1, bin_borders, _ = plt.hist(mass, bins= 35, rwidth = 0)
        bin_centers1 = bin_borders[:-1] + np.diff(bin_borders) / 2
        popt1, pcov1 = curve_fit(model, bin_centers1, bin_heights1,p0=[5.28034916e+03,  1.08696907e+01,  2.66562294e+01,  6.37281297e+05,
                                                                       -2.94043271e+07,  5.60140373e-01, -1.94336327e-03,  4.45021064e-01,
                                                                       3.04197809e+03])
        mass_interval_for_fit = np.linspace(bin_borders[0], bin_borders[-1], 10000)
        background(mass, popt1)
        signal(mass, popt1)
        plt.plot(mass_interval_for_fit, model(mass_interval_for_fit, *popt1), label='fit', color = 'grey')
        yerr = np.sqrt(bin_heights1)
        xerr=(bin_borders[1] - bin_borders[0])/2
        plt.errorbar(bin_centers1, bin_heights1, yerr = yerr,xerr=xerr, fmt = '.', c = 'black', label = 'ML + selection Filtered data')
        #plt.legend()
        plt.xlim ([np.min(mass), np.max(mass)])
        #plt.ylim ([0, np.max(model(mass_interval_for_fit, *popt1))])
        plt.title (r'$q^2$ bin: %i' %q2_bin )
        plt.xlabel (r'$m(K^+ \pi^- \mu^+ \mu^-)$ [MeV/$c^2$]')
        plt.ylabel('Events')
        print (popt1)
        
    plt.figure(figsize=(10,10))
    plt.subplot(4,3,1)
    plot_mass_dist(df_total.to_numpy(), 0)
    plt.subplot(4,3,2)
    plot_mass_dist(df_total.to_numpy(), 1)
    plt.subplot(4,3,3)
    plot_mass_dist(df_total.to_numpy(), 2)
    plt.subplot(4,3,4)
    plot_mass_dist(df_total.to_numpy(), 3)
    plt.subplot(4,3,5)
    plot_mass_dist(df_total.to_numpy(), 4)
    plt.subplot(4,3,6)
    plot_mass_dist(df_total.to_numpy(), 5)
    plt.subplot(4,3,7)
    plot_mass_dist(df_total.to_numpy(), 6)
    plt.subplot(4,3,8)
    plot_mass_dist(df_total.to_numpy(), 7)
    plt.subplot(4,3,9)
    plot_mass_dist(df_total.to_numpy(), 8)
    plt.subplot(4,3,10)
    plot_mass_dist(df_total.to_numpy(), 9)
    
    plt.tight_layout()
    
plot_filtered_data_crystal('data/total_dataset.csv','data/sig.csv','model_depth_3_estimators_200_features_20.json')

    
    
    
    
    
    
    
    
    
    