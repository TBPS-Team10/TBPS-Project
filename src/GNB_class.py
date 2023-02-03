#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 22:13:36 2023

@author: emilyip
"""

import numpy as np
import pandas as pd


def calculate_prior_probabilities(df):
    prior_probabilities = df.groupby(by='event').apply(lambda x: len(x) / len(df))
    return np.log(prior_probabilities).values


def return_statistics(df):
    mean = df.groupby(by='event').apply(lambda x: x.mean(axis=0))
    variance = df.groupby(by='event').apply(lambda x: x.var(axis=0))
    return mean.values, variance.values


def calculate_probability_density(mean, variance, x):
    probability_density = (1 / np.sqrt(2 * np.pi * variance)) * np.exp((-(x - mean) ** 2) / (2 * variance))
    return probability_density


def calculate_posterior_probabilities(df_row, mean, variance, n_unique_labels, n_cols):
    posterior_probabilities = []
    for i in range(n_unique_labels):
        posterior = 0
        for j in range(n_cols):
            posterior += np.log(calculate_probability_density(mean[i][j], variance[i][j], df_row[j]))
        posterior_probabilities.append(posterior)
    return posterior_probabilities


def NBA_fit(df):
    n_cols = len(df.columns) - 1
    unique_labels = df['event'].unique()
    n_unique_labels = len(unique_labels)
    mean, variance = return_statistics(df)
    prior_probabilities = calculate_prior_probabilities(df)  # returns log
    return {
        'n_cols': n_cols,
        'unique_labels': unique_labels,
        'n_unique_labels': n_unique_labels,
        'mean': mean,
        'variance': variance,
        'prior_probabilities': prior_probabilities}


def predict(test_df, nba):
    predictions = []
    for i in range(len(test_df)):
        prior = nba['prior_probabilities']
        posterior = calculate_posterior_probabilities(test_df.iloc[i, :-1], nba['mean'], nba['variance'],
                                                      nba['n_unique_labels'], nba['n_cols'])  # returns log
        probabilities = prior + posterior
        # one with max prob will be the output 
        mx_idx = np.argmax(probabilities)
        res = nba['unique_labels'][mx_idx]
        predictions.append(res)  # add log values
        print(res)
    return predictions
