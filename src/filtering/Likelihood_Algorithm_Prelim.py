import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import scipy.optimize as op


#%%

data_path = r"C:\Users\Yuqing\OneDrive - Imperial College London\Team-Based Problem Solving\TBPS - Spring 2023\\"

sig = pd.read_csv(data_path + 'sig.csv')


#%%

# Concatenate all unwanted datasets using this
"""
fake_datanames = ['jpsi.csv', 'psi2S.csv', 'jpsi_mu_k_swap.csv', 'jpsi_mu_pi_swap.csv', 'k_pi_swap.csv', 'phimumu.csv',
    'pKmumu_piTok_kTop.csv', 'pKmumu_piTop.csv', 'Kmumu.csv', 'Kstarp_pi0.csv', 'Jpsi_Kstarp_pi0.csv']

for i in range(len(fake_datanames)):
    name = fake_datanames[i]
    if i==0:
        unwanted = pd.read_csv(data_path + name)
    else:
        new_data = pd.read_csv(data_path + name)
        unwanted = pd.concat([unwanted, new_data], axis=0)
"""

unwanted = pd.read_csv('other_decay_channels.csv')


#%%

# This thing is gigantic so I'll work with a smaller sample
unwanted = unwanted.sample(500000)

# Modify this line in final run

# The method .sample adds an extra column for some reason?? This doesn't
# affect the other stuff though so I'll leave it alone


#%%

# Which variables to filter for?
gauss_vars = ['B0_M', 'Kstar_M']
exp_vars = ['B0_IPCHI2_OWNPV', 'J_psi_ENDVERTEX_CHI2', 'Kstar_ENDVERTEX_CHI2']
invexp_vars = ['mu_plus_ProbNNmu', 'mu_minus_ProbNNmu', 'K_ProbNNk', 'Pi_ProbNNpi',
        'B0_DIRA_OWNPV']


#%%

# GAUSSIAN

gauss_params = [[],[]]

for var in gauss_vars:
    dataset = sig[var]
    gauss_params[0].append(np.mean(dataset))
    gauss_params[1].append(np.std(dataset))


#%%

# EXPONENTIAL

def model_exp(x, n0, grad):
    return n0 * np.e ** (grad*x)


# Analyse removing 10% in the tail (some arbitrary decision I made)
def get_binning(var, sig=sig, bins=50, percentile=0.90, remove_neg=True):
    dataset = sig[var]
    # Remove_neg deals with -1000 probs
    if remove_neg:
        dataset = dataset[np.where(dataset>=0, True, False)]
    sorted_var = np.sort(dataset)
    # Pick first percentile percent
    sorted_var = sorted_var[0:int(len(sorted_var)*percentile)]
    n, bins, patches = plt.hist(sorted_var, bins=bins)
    return n, bins


def fit_exp(var, sig=sig, bins=50, percentile=0.90, remove_neg=True):
    n, binning = get_binning(var, sig=sig, bins=bins, percentile=percentile, remove_neg=remove_neg)
    
    # Guess parameters. Set x to linspace - normalise this later
    x_axis = np.linspace(0,bins-1, num=bins)
    n0_guess = n[0]
    grad_guess = -1 * np.log(n[1]/n[11]) / 10
    
    # Calc uncertainties. I just assumed unc=1 if 0 data points
    if min(n)>=0:
        unc = np.sqrt(n)
    else:
        unc = np.zeros_like(n)
        for i in range(len(n)):
            if n[i]>=0:
                unc[i] = np.sqrt(n[i])
            else:
                unc[i] = 1
    
    popt = op.curve_fit(model_exp, x_axis, n, p0=[n0_guess, grad_guess], sigma=unc)
    opt_params = popt[0]
    
    x_sep = (binning[-1] - binning[0]) / bins
    decay_rate = opt_params[1] / x_sep
    
    # Decay rate defined in units of true x-axis
    return decay_rate


exp_params = []

for var in exp_vars:
    #print(var)
    result = fit_exp(var)
    exp_params.append(result)
# This plots a histogram, this is because I used plt.hist() to get bins
# Ignore this plot


#%%

# EXPONENTIAL TOWARDS 1

def get_invexp_binning(var, sig=sig, bins=50, percentile=0.90, remove_neg=True):
    dataset = sig[var]
    if remove_neg:
        dataset = dataset[np.where(dataset>=0, True, False)]
    # This just bins 1-dataset
    dataset = 1 - dataset
    sorted_var = np.sort(dataset)
    sorted_var = sorted_var[0:int(len(sorted_var)*percentile)]
    n, bins, patches = plt.hist(sorted_var, bins=bins)
    return n, bins


def fit_invexp(var, sig=sig, bins=50, percentile=0.90, remove_neg=True):
    n, binning = get_invexp_binning(var, sig=sig, bins=bins, percentile=percentile, remove_neg=remove_neg)
    
    x_axis = np.linspace(0,bins-1, num=bins)
    n0_guess = n[0]
    grad_guess = -1 * np.log(n[1]/n[11]) / 10
    
    if min(n)>=0:
        unc = np.sqrt(n)
    else:
        unc = np.zeros_like(n)
        for i in range(len(n)):
            if n[i]>=0:
                unc[i] = np.sqrt(n[i])
            else:
                unc[i] = 1
    
    popt = op.curve_fit(model_exp, x_axis, n, p0=[n0_guess, grad_guess], sigma=unc)
    opt_params = popt[0]
    
    x_sep = (binning[-1] - binning[0]) / bins
    decay_rate = opt_params[1] / x_sep
    
    return decay_rate


invexp_params = []

for var in invexp_vars:
    #print(var)
    result = fit_invexp(var)
    invexp_params.append(result)


#%%

# Save everything to avoid regenerating stuff

np.save('gauss_vars', gauss_vars)
np.save('exp_vars', exp_vars)
np.save('invexp_vars', invexp_vars)

np.save('gauss_params', gauss_params)
np.save('exp_params', exp_params)
np.save('invexp_params', invexp_params)


#%%

# Calculate log-likelihood
# Calculates log of likelihood despite what the name says

def calc_gauss_likelihood(data, normalisations, gauss_vars, gauss_params):
    likelihoods = np.zeros(len(data))
    for i in range(len(gauss_vars)):
        variables = data[gauss_vars[i]]
        # print('Adding' + gauss_vars[i], gauss_params[0][i], gauss_params[1][i])
        gauss_likelihood = -1 * (variables - gauss_params[0][i])**2 / (2* gauss_params[1][i]**2)
        likelihoods += normalisations[i] * gauss_likelihood
    return likelihoods


def calc_exp_likelihood(data, normalisations, exp_vars, exp_params):
    likelihoods = np.zeros(len(data))
    
    for i in range(len(exp_vars)):
        #print(exp_vars[i])
        variables = data[exp_vars[i]]
        # Deals with -1000 issue
        if min(variables)<0:
            for i in range(len(variables)):
                if variables[i]<0:
                    variables[i]=0
        exp_likelihood = variables * exp_params[i]
        likelihoods += normalisations[i] * exp_likelihood
    return likelihoods


def calc_invexp_likelihood(data, normalisations, invexp_vars, invexp_params):
    likelihoods = np.zeros(len(data))
    
    for i in range(len(invexp_vars)):
        #print(invexp_vars[i])
        variables = data[invexp_vars[i]]
        invexp_likelihood = (1-variables) * invexp_params[i]
        likelihoods += normalisations[i] * invexp_likelihood
    return likelihoods


#%%

def calc_log_likelihood(data, normalisations=None,
        variables=[gauss_vars, exp_vars, invexp_vars], parameters=[gauss_params, exp_params, invexp_params]):
    
    if normalisations==None:
        # Sets everything to weighting 1
        normalisations = []
        for var_ls in variables:
            normalisations.append(np.ones(len(var_ls)))
    #print(normalisations)
    likelihoods = np.zeros(len(data))
    
    likelihoods += calc_gauss_likelihood(data, normalisations[0], variables[0], parameters[0])
    likelihoods += calc_exp_likelihood(data, normalisations[1], variables[1], parameters[1])
    likelihoods += calc_invexp_likelihood(data, normalisations[2], variables[2], parameters[2])
    return likelihoods


#%%

# Gives cutoff for log-likelihoods
def return_cutoff(normalisations=None, percentile=0.01, sig=sig, variables=[gauss_vars, exp_vars, invexp_vars],
        parameters=[gauss_params, exp_params, invexp_params]):
    log_likelihoods = calc_log_likelihood(sig, normalisations, variables, parameters)
    sorted_logs = np.sort(log_likelihoods)
    return sorted_logs[int(percentile*len(log_likelihoods))]


# Count how many were removed
def return_passed(cutoff, normalisations=None, unwanted=unwanted, variables=[gauss_vars, exp_vars, invexp_vars],
        parameters=[gauss_params, exp_params, invexp_params]):
    log_likelihoods = calc_log_likelihood(unwanted, normalisations, variables, parameters)
    passed = unwanted[np.where(log_likelihoods>cutoff, True, False)]
    return passed


#%%

# Index the parameters by list of 9 parameters (fix B0_M as weight 1 because
# changes in relative normalisations don't affect the final result)

# I am going to hard code in the 2+3+5 parameter list - change if needed

trial_params = np.array([0.7, 0.05, 0.05, 0.05, 0.03, 0.03, 0.03, 0.03, 0.03])
# Give Kstar a 0.5 weighting and downweight everything else


def list_to_normalisations(trial_params):
    gauss_weights = np.array([1, trial_params[0]])
    exp_weights = trial_params[1: 4]
    invexp_weights = trial_params[4: 9]
    return [gauss_weights, exp_weights, invexp_weights]


def likelihood_filter(trial_params, percentile=0.01, sig=sig, unwanted=unwanted,
        variables=[gauss_vars, exp_vars, invexp_vars],
        parameters=[gauss_params, exp_params, invexp_params]):
    """
    Filter the dataset, returns data that passes through the filter
    """
    trial_normalisations = list_to_normalisations(trial_params)
    
    # Predict the cutoff needed
    pred_cutoff = return_cutoff(normalisations=trial_normalisations, sig=sig, percentile=percentile,
            variables=[gauss_vars, exp_vars, invexp_vars], parameters=[gauss_params, exp_params, invexp_params])
    #print(pred_cutoff)
    
    passed = return_passed(pred_cutoff, normalisations=trial_normalisations,
            unwanted=unwanted, variables=[gauss_vars, exp_vars, invexp_vars],
            parameters=[gauss_params, exp_params, invexp_params])
    
    return passed


def prop_surviving(trial_params, percentile=0.01, sig=sig, unwanted=unwanted,
        variables=[gauss_vars, exp_vars, invexp_vars],
        parameters=[gauss_params, exp_params, invexp_params]):
    """
    Count proportion that is deleted
    """
    passed = likelihood_filter(trial_params, percentile=percentile, sig=sig, unwanted=unwanted,
        variables=[gauss_vars, exp_vars, invexp_vars],
        parameters=[gauss_params, exp_params, invexp_params])
    
    frac_surviving = len(passed) / len(unwanted)
    
    return frac_surviving


num_removed = prop_surviving(trial_params)


#%%

# Task: optimise the numbers in trial_params
params_guess = np.array([0.7, 0.05, 0.05, 0.05, 0.03, 0.03, 0.03, 0.03, 0.03])

bestfit = op.minimize(prop_surviving, params_guess, method='COBYLA', options={"maxiter":100})
# COBYLA seems to be fastest and gives decent estimates


#%%

params_optimized = bestfit.x

print(prop_surviving(params_optimized))
print(prop_surviving(params_optimized, unwanted=sig))

np.save('params_likelihoodsorter', params_optimized)




# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

