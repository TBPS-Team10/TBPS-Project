#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:58:01 2023

@author: aisulu
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import mpl_scatter_density # adds projection='scatter_density'
from matplotlib.colors import LinearSegmentedColormap
from scipy.optimize import curve_fit
import Finalised_filters as fil
import model_XGB as mod
import Likelihood_Algorithm_Final as laf
import seaborn as sns
import math
from scipy.integrate import quad

plt.style.use("bmh")

plt.rcParams.update({
    "figure.figsize": (8, 5),
    "font.serif": ["Times"],
    "legend.fontsize": 18,
    "axes.labelsize": 20,
    "axes.titlesize": 18,
    "xtick.labelsize": 18,
    "ytick.labelsize": 18,
    "font.family": "serif"})
def ML(data_path,ML_model_json, features):
    bdt_model = mod.BDT_model()
    bdt_model.load_model(ML_model_json)
    bdt_model.specify_feature_num(20)
    feature_list = np.loadtxt(features, delimiter = ',', dtype = 'int32')
    bdt_model.specify_features(feature_list)
    
    data_df = pd.read_csv(data_path)
    fil.cut_q2(data_df)
    data = data_df.to_numpy()
    init_len = len(data)
    print (init_len)
    test_data = bdt_model.predict(data)
    
    indices = []
    for i in range (len(test_data)):
        if test_data[i] != 0:
            indices.append(i)
    
    clean_data = np.delete(data, (indices), axis = 0)
    final_len = len(clean_data)
    print (final_len)
    accuracy = final_len/init_len * 100
    return accuracy, test_data

def filter_and_ML(signal, total, ML_model_json, features):
    variables = pd.read_csv(signal)
    variables = list(variables.columns)
    
    bdt_model = mod.BDT_model()
    bdt_model.load_model(ML_model_json)
    bdt_model.specify_feature_num(20)
    feature_list = np.loadtxt(features, delimiter = ',', dtype = 'int32')
    bdt_model.specify_features(feature_list)
    
    total_dataset = pd.read_csv(total)
    fil.filter_light(pd.read_csv(signal), total_dataset)
    total_dataset_filtered = laf.likelihood_filter_final(total_dataset)
    
    test_total_dataset = bdt_model.predict(total_dataset_filtered.to_numpy())
    
    indices = []
    for i in range (len(test_total_dataset)):
        if test_total_dataset[i] != 0:
            indices.append(i)
    clean_total_dataset = np.delete(total_dataset_filtered.to_numpy(), (indices), axis = 0)
    return clean_total_dataset
#%%
variables = pd.read_csv('data/sig.csv')
variables = list(variables.columns)
#df = filter_and_ML('data/sig.csv', 'data/jpsi.csv', 'post_filter_ML_20_features copy.json', 'post_filter_ML_20_features copy.csv')
df = pd.read_csv('data/total_dataset.csv')
df.drop(df[(df['q2'] < 8.0)].index, inplace=True)
df.drop(df[(df['q2'] > 11.0)].index, inplace=True)
jpsi = df
plt.hist(jpsi['B0_M'], bins =np.linspace(5170,5700,50))
#%%
plt.hist(jpsi['q2'], bins =35)
#%%
def exp(x, A, tau):
    return A * np.exp(-tau*(x-5280))

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

def model (mass , amplitude_sig, mean, std1, std2, alpha, n, f,amplitude_exp, tau):
    sig = signal_model(mass, mean, std1, std2, alpha, n, f,amplitude_sig)
    bg = exp(mass, amplitude_exp, tau)
    return sig + bg

def signal(mass, popt1):
    x = np.linspace(np.min(mass),np.max(mass),10000)
    y = signal_model (x, popt1[1], popt1[2], popt1[3],popt1[4],popt1[5],popt1[6],popt1[0])
    plt.plot(x, y, color = '#539ecd')
    plt.fill_between(x, y, 0, color='#539ecd', label = 'Signal', alpha = 0.5)
def background (mass, popt1):
    x = np.linspace(np.min(mass),np.max(mass),10000)
    y = exp (x, popt1[7], popt1[8])
    plt.plot(x, y, color = 'red')
    plt.fill_between(x, y, 0,color = 'red',facecolor = 'none', label = 'Background', alpha = 0.5,hatch= r'\\\\' )
def signal_y(mass, y):
    x = mass
    plt.plot(x, y, color = '#539ecd')
    plt.fill_between(x, y, 0, color='#539ecd', label = 'Signal', alpha = 0.5)
def background_y(mass, y):
    x = mass
    plt.plot(x, y, color = 'red')
    plt.fill_between(x, y, 0,color = 'red',facecolor = 'none', label = 'Background', alpha = 0.5,hatch= r'\\\\' )
#%%
jpsi_mass = jpsi['B0_M']
jpsi_upper = []
for mass in jpsi_mass:
    if mass > 5600:
       jpsi_upper.append(mass)
bin_heights1, bin_borders, _ = plt.hist(jpsi_upper, bins= 10, rwidth = 0)
bin_centers1 = bin_borders[:-1] + np.diff(bin_borders) / 2
p0 = [170, 4e-3] 
popt, popt_cov = curve_fit(exp, bin_centers1, bin_heights1,p0 = p0)
xs = np.linspace(min(jpsi_upper), max(jpsi_upper), 50)
yerr = np.sqrt(bin_heights1)
xerr=(bin_borders[1] - bin_borders[0])/2
plt.errorbar(bin_centers1, bin_heights1, yerr = yerr,xerr = xerr, fmt = '.', c = 'black')
plt.plot(xs, exp(xs, *popt), label='Background fit', color = 'grey')
plt.ylabel (r'$q^2$')
plt.xlabel (r'$m_{K^+ \pi^- \mu^+ \mu^-}$ [MeV/$c^2$]')
plt.legend()
plt.tight_layout()
plt.savefig("Plots_fitting/Backgroundfit.svg", format="svg")
plt.savefig("Plots_fitting/Backgroundfit.pdf", format="pdf")
print (popt)
print (np.sqrt (popt_cov[0][0]), np.sqrt (popt_cov[1][1]))
#%%
def print_coef(popt, popt_cov):
    print ('Amplitude_sig = %.4e +- %.3e' %(popt[0], np.sqrt(popt_cov[0][0])))
    print ('Mean = %.4e +- %.4e' %(popt[1], np.sqrt(popt_cov[1][1])))
    print ('Sigma 1= %.3e +- %.3e' %(popt[2], np.sqrt(popt_cov[2][2])))
    print ('Sigma 2 = %.3e +- %.3e' %(popt[3], np.sqrt(popt_cov[3][3])))
    print ('Alpha = %.4e +- %.3e' %(popt[4], np.sqrt(popt_cov[4][4])))
    print ('n = %.3e +- %.3e' %(popt[5], np.sqrt(popt_cov[5][5])))
    print ('f core = %.3e +- %.3e' %(popt[6], np.sqrt(popt_cov[6][6])))
    print ('Amplitude_bg = %.3e +- %.3e' %(popt[7], np.sqrt(popt_cov[7][7])))
    print ('tau = %.3e +- %.3e' %(popt[8], np.sqrt(popt_cov[8][8])))
#[ amplitude_sig, mean, std1, std2, alpha, n, f, amplitude_exp, tau]
p0 = [6e5, 5280, 15, 26, 1.5, 5.2, 0.7, popt[0], popt[1]]
bounds = [(-np.inf, np.inf)]*len(p0)
bounds[2] = (10, 20)
bounds[3] = (10, 50)
bounds[4] = (1, 2)
bounds[5] = (3, 5.3)
bounds[6] = (0.5, 1)
bounds[8] = (3e-3, 6e-3)
bin_heights1, bin_borders, _ = plt.hist(jpsi_mass, bins= 35, rwidth = 0)
bin_centers1 = bin_borders[:-1] + np.diff(bin_borders) / 2
popt1, popt_cov1 = curve_fit(model, bin_centers1, bin_heights1, p0 = p0, absolute_sigma=True,
                             bounds=tuple(zip(*bounds)), method='trf',
                             jac='3-point')
xs = np.linspace(min(jpsi_mass), max(jpsi_mass), 500)
yerr = np.sqrt(bin_heights1)
xerr=(bin_borders[1] - bin_borders[0])/2
plt.errorbar(bin_centers1, bin_heights1, yerr = yerr,xerr = xerr, fmt = '.', c = 'black')
signal(xs,popt1)
background(xs, popt1)
plt.plot(xs, model(xs, *popt1), label='Signal + background fit', color = 'black')
plt.ylabel (r'$q^2$')
plt.xlabel (r'$m_{K^+ \pi^- \mu^+ \mu^-}$ [MeV/$c^2$]')
#plt.legend()
plt.text (5570,6.3e4, r'$B^0 \rightarrow J/\psi K^{*0}$',fontfamily = 'Times', fontsize = 20)
plt.tight_layout()
plt.savefig("Plots_fitting/Backgroundsigfit.svg", format="svg")
plt.savefig("Plots_fitting/Backgroundsigfit.pdf", format="pdf")

print (popt1)
print_coef(popt1, popt_cov1)
popt1_copy = np.copy(popt1)
#%%
signal_df = pd.read_csv('data/sig.csv')
sig_mass_df = signal_df['B0_M']
#%%
sigma_scales = []
sigma_scales_err = []
def get_bin(data, q2_bin):
    q2_bins = [[0.1, 0.98], [1.1, 2.5], [2.5, 4.0], [4.0, 6.0], [6.0, 8.0], 
               [15.0, 17.0], [17.0, 19.0], [11.0, 12.5], [1.0, 6.0], [15.0, 19.0]]
    q = data[q2_bins[q2_bin][0] < data[:,90]]
    q = q[q[:,90] < q2_bins[q2_bin][1]]
    mass = q[:,56]
    return mass
def scaled_sigma(popt1):
    popt = np.copy(popt1)
    sigma1 = popt[2]
    sigma2 = popt[3]
    def new_sig(m, A, scale):
        popt[2] = scale*sigma1
        popt[3] = scale*sigma2
        return A*signal_model(m,popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[0])
    return new_sig
for i in range(10):
    p0 = [0.05, 1]
    bin_heights, bin_borders, _ = plt.hist(get_bin(signal_df.to_numpy(), i), bins=np.linspace(5170,5700,35), rwidth = 0)
    bin_centers = bin_borders[:-1] + np.diff(bin_borders) / 2
    popt2, popt_cov2 = curve_fit(scaled_sigma(popt1), bin_centers, bin_heights, p0=p0)
    xs = np.linspace(5170,5700,500)
    yerr = np.sqrt(bin_heights)
    xerr=(bin_borders[1] - bin_borders[0])/2
    plt.errorbar(bin_centers, bin_heights, yerr = yerr,xerr = xerr, fmt = '.', c = 'black')
    plt.plot(xs, scaled_sigma(popt1)(xs, *popt2), label=r'Fine-tuned $\sigma$ ', color = 'black')
    sigma_scales.append(popt2[1])
    sigma_scales_err.append(np.sqrt(popt_cov2[1][1]))
    plt.plot(xs, popt2[0]*signal_model(xs, popt1[1], popt1[2], popt1[3], popt1[4], popt1[5], popt1[6], popt1[0]), '--', color = 'red', alpha = 0.5, label =r'Initial $\sigma$')
    plt.legend()
    plt.ylabel (r'$q^2$')
    plt.xlabel (r'$m_{K^+ \pi^- \mu^+ \mu^-}$ [MeV/$c^2$]')
    plt.tight_layout()
    plt.show()
    plt.savefig(f"Plots_fitting/finetune{i}.svg", format="svg")
    plt.savefig(f"Plots_fitting/finetune{i}.pdf", format="pdf")
    plt.close()
#%%
p0 = [0.05, 1]
bin_heights, bin_borders, _ = plt.hist(get_bin(signal_df.to_numpy(), 0), bins=np.linspace(5170,5700,35), rwidth = 0)
bin_centers = bin_borders[:-1] + np.diff(bin_borders) / 2
popt2, popt_cov2 = curve_fit(scaled_sigma(popt1), bin_centers, bin_heights, p0=p0)
xs = np.linspace(5170,5700,500)
yerr = np.sqrt(bin_heights)
xerr=(bin_borders[1] - bin_borders[0])/2
plt.errorbar(bin_centers, bin_heights, yerr = yerr,xerr = xerr, fmt = '.', c = 'black')
plt.plot(xs, scaled_sigma(popt1)(xs, *popt2), label=r'Fine-tuned $\sigma$ ', color = 'black')
sigma_scales.append(popt2[1])
sigma_scales_err.append(np.sqrt(popt_cov2[1][1]))
plt.plot(xs, popt2[0]*signal_model(xs, popt1[1], popt1[2], popt1[3], popt1[4], popt1[5], popt1[6], popt1[0]), '--', color = 'red', alpha = 0.5, label =r'Initial $\sigma$')
plt.legend()
plt.ylabel (r'$q^2$')
plt.xlabel (r'$m_{K^+ \pi^- \mu^+ \mu^-}$ [MeV/$c^2$]')
plt.tight_layout()
#%%
print(sigma_scales)
print (sigma_scales_err)
#%%
total = filter_and_ML('data/sig.csv', 'data/total_dataset.csv','filters_24.02.2023_features_20_depth_3_estimators_200 copy.json', 'filters_24.02.2023_features_20_depth_3_estimators_200_feature_list copy.csv')
#%%
for i in range(10):
    def scaled_sigma_full(popt1):
        popt = np.copy(popt1)
        sigma1 = popt[2]
        sigma2 = popt[3]
        def new(m, A):
            popt[2] = sigma_scales[i]*sigma1
            popt[3] = sigma_scales[i]*sigma2
            return A*model(m, *popt)
        return new
    bin_heights, bin_borders, _ = plt.hist(get_bin(total, 0), bins=np.linspace(5170,5700,40), rwidth = 0)
    bin_centers = bin_borders[:-1] + np.diff(bin_borders) / 2
    popt3, poopt_cov3 = curve_fit(scaled_sigma_full(popt1), bin_centers, bin_heights)
    xs = np.linspace(5170,5700,500)
    yerr = np.sqrt(bin_heights)
    xerr=(bin_borders[1] - bin_borders[0])/2
    plt.errorbar(bin_centers, bin_heights, yerr = yerr,xerr = xerr, fmt = '.', c = 'black')
    print (popt3)
    signal_y(xs, popt3*signal_model(xs, popt1[1], sigma_scales[i]*popt1[2], sigma_scales[i]*popt1[3], popt1[4], popt1[5], popt1[6], popt1[0]) )
    background_y (xs, popt3*exp(xs, popt1[7], popt1[8]))
    plt.plot(xs, scaled_sigma_full(popt1)(xs, *popt3), color = 'black')
    plt.legend()
    plt.ylabel (r'$q^2$')
    plt.xlabel (r'$m_{K^+ \pi^- \mu^+ \mu^-}$ [MeV/$c^2$]')
    plt.tight_layout()
    plt.show()
    plt.savefig(f"Plots_fitting/totalfit{i}.svg", format="svg")
    plt.savefig(f"Plots_fitting/totalfit{i}.pdf", format="pdf")
    plt.close()
#%%
for i in range(10):
    def scaled_sigma_full(popt1):
        popt = np.copy(popt1)
        sigma1 = popt[2]
        sigma2 = popt[3]
        def new(m, A):
            popt[2] = sigma_scales[i]*sigma1
            popt[3] = sigma_scales[i]*sigma2
            return A*model(m, *popt)
        return new
    bin_heights, bin_borders, _ = plt.hist(get_bin(total, 0), bins=np.linspace(5170,5700,40), rwidth = 0)
    bin_centers = bin_borders[:-1] + np.diff(bin_borders) / 2
    popt3, poopt_cov3 = curve_fit(scaled_sigma_full(popt1), bin_centers, bin_heights)
    xs = np.linspace(5170,5700,500)
    total_area = quad(lambda m:scaled_sigma_full(popt1)(m, *popt3), min(xs), max(xs))
    total_area_err = total_area[1]/total_area[0]*100
    bg_area = quad(lambda m:popt3*exp(m, popt1[7], popt1[8]), min(xs), max(xs))
    bg_area_err = bg_area[1]/bg_area[0]*100
    signal_area = quad(lambda m: popt3*signal_model(m, popt1[1], sigma_scales[i]*popt1[2], sigma_scales[i]*popt1[3], popt1[4], popt1[5], popt1[6], popt1[0]), min(xs), max(xs) )
    sig_area_err = signal_area[1]/signal_area[0]*100
    bg_perc = bg_area[0]/total_area[0] * 100
    bg_err = bg_area_err + total_area_err
    sig_perc = signal_area[0]/total_area[0] * 100
    sig_err = sig_area_err + total_area_err
    print ('Bin: %.i, bgd = %.3f +- %.3f persent' %(i, bg_perc, bg_err))
    print ('Bin: %.i, sig = %.3f +- %.3f percent' %(i, sig_perc, sig_err))

#%%
accuracy, test_data = ML('data/sig.csv','filters_24.02.2023_features_20_depth_3_estimators_200 copy.json', 'filters_24.02.2023_features_20_depth_3_estimators_200_feature_list copy.csv' )
print (accuracy)
accuracy1, test_data1 = ML('data/sig.csv','post_filter_ML_20_features copy.json', 'post_filter_ML_20_features copy.csv' )
print (accuracy1)
#%%
def using_mpl_scatter_density(fig, x, y):
    ax = fig.add_subplot(1, 1, 1, projection='scatter_density')
    white_viridis = LinearSegmentedColormap.from_list('white_viridis', [
        (0, '#ffffff'),
        (1e-20, '#440053'),
        (0.2, '#404388'),
        (0.4, '#2a788e'),
        (0.6, '#21a784'),
        (0.8, '#78d151'),
        (1, '#fde624'),
    ], N=len(y))
    density = ax.scatter_density(x, y, cmap=white_viridis)
    fig.colorbar(density, label='Number of points per pixel')

def plot(data, name):
    x = data['B0_M'] 
    y = data['q2']

    fig = plt.figure()
    using_mpl_scatter_density(fig, x, y)
    plt.ylabel ('q2')
    plt.xlabel ('B0_M')
    plt.title (name)
    plt.show()



#%%
















