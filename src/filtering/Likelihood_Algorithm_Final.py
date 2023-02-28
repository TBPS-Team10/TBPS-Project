import numpy as np
import pandas as pd


"""
If running as some part of other code, import likelihood_filter_final and call:
    data = likelihood_filter_final(data)
"""


#%%

data_path = r"C:\Users\Yuqing\OneDrive - Imperial College London\Team-Based Problem Solving\TBPS - Spring 2023\\"

sig = pd.read_csv(data_path + 'sig.csv')


#%%

gauss_vars = np.load('gauss_vars.npy')
exp_vars = np.load('exp_vars.npy')
invexp_vars = np.load('invexp_vars.npy')

gauss_params = np.load('gauss_params.npy')
exp_params = np.load('exp_params.npy')
invexp_params = np.load('invexp_params.npy')

params_optimized = np.load('params_likelihoodsorter.npy')


#%%

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
def return_passed(cutoff, data, normalisations=None, variables=[gauss_vars, exp_vars, invexp_vars],
        parameters=[gauss_params, exp_params, invexp_params]):
    log_likelihoods = calc_log_likelihood(data, normalisations, variables, parameters)
    passed = data[np.where(log_likelihoods>cutoff, True, False)]
    return passed


def list_to_normalisations(trial_params):
    gauss_weights = np.array([1, trial_params[0]])
    exp_weights = trial_params[1: 4]
    invexp_weights = trial_params[4: 9]
    return [gauss_weights, exp_weights, invexp_weights]


"""
Here is the function you need:
"""

def likelihood_filter(trial_params, data, percentile=0.01, sig=sig,
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
    
    passed = return_passed(pred_cutoff, data, normalisations=trial_normalisations,
            variables=[gauss_vars, exp_vars, invexp_vars],
            parameters=[gauss_params, exp_params, invexp_params])
    
    return passed


def prop_surviving(trial_params, data, percentile=0.01, sig=sig,
        variables=[gauss_vars, exp_vars, invexp_vars],
        parameters=[gauss_params, exp_params, invexp_params]):
    """
    Count proportion that is deleted
    """
    passed = likelihood_filter(trial_params, data, percentile=percentile, sig=sig,
        variables=[gauss_vars, exp_vars, invexp_vars],
        parameters=[gauss_params, exp_params, invexp_params])
    
    frac_surviving = len(passed) / len(data)
    
    return frac_surviving


#%%

# unwanted = pd.read_csv('other_decay_channels.csv')

# print(prop_surviving(params_optimized, data=unwanted))
# This keeps about 64% of the unwanted dataset

def likelihood_filter_final(data):
    return likelihood_filter(params_optimized, data)

# filtered_data = likelihood_filter_final(unwanted)


# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 23:30:55 2023

@author: Yuqing
"""

