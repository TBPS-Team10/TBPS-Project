#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 11:46:44 2023

@author: aisulu
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import Likelihood_Algorithm_Final as laf


def cut_IPCHI2_OWNPV(df):
    df.drop(df[(df['B0_IPCHI2_OWNPV'] > 15.996)].index, inplace=True)
    df.drop(df[(df['mu_plus_IPCHI2_OWNPV'] < 6.0107)].index, inplace=True)
    df.drop(df[(df['mu_minus_IPCHI2_OWNPV'] < 6.0005)].index, inplace=True)
    df.drop(df[(df['K_IPCHI2_OWNPV'] < 6.00087)].index, inplace=True)
    df.drop(df[(df['Pi_IPCHI2_OWNPV'] < 6.000345)].index, inplace=True)
def cut_PV(df):
    df.drop(df[(df['B0_OWNPV_X'] - np.mean(df['B0_OWNPV_X']) < -0.1645)].index, inplace=True)
    df.drop(df[(df['B0_OWNPV_X'] - np.mean(df['B0_OWNPV_X']) > 0.1811)].index, inplace=True)
    df.drop(df[(df['B0_OWNPV_Y'] - np.mean(df['B0_OWNPV_Y']) < -0.1965)].index, inplace=True)
    df.drop(df[(df['B0_OWNPV_Y'] - np.mean(df['B0_OWNPV_Y']) > 0.17294)].index, inplace=True)
    df.drop(df[(df['B0_OWNPV_Z'] - np.mean(df['B0_OWNPV_Z']) < -170.5154)].index, inplace=True)
    df.drop(df[(df['B0_OWNPV_Z'] - np.mean(df['B0_OWNPV_Z']) > 165.988)].index, inplace=True)
def cut_probs (df):
    df.drop(df[(df['K_ProbNNk'] < 3.746e-05)].index, inplace=True)
    df.drop(df[(df['Pi_ProbNNpi'] <  0.00099)].index, inplace=True)
    df.drop(df[(df['mu_plus_ProbNNmu'] < 0.0024)].index, inplace=True)
    df.drop(df[(df['mu_minus_ProbNNmu'] <  0.000895)].index, inplace=True)
def cut_theta_sep(df):
    df.drop(df[(abs(df['mu_plus_ETA']-df['mu_minus_ETA']) < 0.0001)].index, inplace=True)
    df.drop(df[(abs(df['mu_plus_ETA']-df['K_ETA']) < 0.0001)].index, inplace=True)
    df.drop(df[(abs(df['mu_plus_ETA']-df['Pi_ETA']) < 0.0001)].index, inplace=True)
    df.drop(df[(abs(df['mu_minus_ETA']-df['K_ETA']) < 0.0001)].index, inplace=True)
    df.drop(df[(abs(df['mu_minus_ETA']-df['Pi_ETA']) < 0.0001)].index, inplace=True)
    df.drop(df[(abs(df['K_ETA']-df['Pi_ETA']) < 0.0001)].index, inplace=True)
def cut_DIRA(df):
    df.drop(df[(df['B0_DIRA_OWNPV'] < 0.99990)].index, inplace=True)
def cut_K_mass(df):
    mean = np.mean(df['Kstar_M'])
    sigma = np.std (df['Kstar_M'])
    lower_range = mean-(5*sigma)
    upper_range = mean+(5*sigma)
    df.drop(df[(df['Kstar_M'] < lower_range)].index, inplace=True)
    df.drop(df[(df['Kstar_M'] > upper_range)].index, inplace=True)
def cut_FDCHI(df):
    df.drop(df[(df['B0_FDCHI2_OWNPV'] < 64.084)].index, inplace=True)
    df.drop(df[(df['Kstar_FDCHI2_OWNPV'] < 16.0011)].index, inplace=True)
def cut_phimumu(df):
    df.drop(df[(df['Pi_ProbNNpi'] -df['Pi_ProbNNk'] < 0.75)&(df['Kstar_M'] > 745)&(df['Kstar_M'] < 1095)
              &(df['B0_M'] > 5170)&(df['B0_M'] < 5698)].index, inplace = True)
    mean = 8.45561878e-01
    sigma = 6.67542976e-01
    lower_range = mean-(3*sigma)
    upper_range = mean+(3*sigma)
    df.drop(df[(df['B0_ENDVERTEX_X'] < lower_range)].index, inplace=True)
    df.drop(df[(df['B0_ENDVERTEX_X'] > upper_range)].index, inplace=True)
def cut_Kmumu(df): #38% of kmumu decays are not filtered
    mean = 896.71732264
    sigma = 26.35192252
    lower_range = mean-(3*sigma)
    upper_range = mean+(3*sigma)
    df.drop(df[(df['Kstar_M'] < lower_range)].index, inplace=True)
    df.drop(df[(df['Kstar_M'] > upper_range)].index, inplace=True)
    df.drop(df[(df['J_psi_M'] > 4382)].index, inplace=True)
    mean = -1.79634433e-01
    sigma = 3.29470538e-02
    lower_range = mean-(3*sigma)
    upper_range = mean+(3*sigma)
    df.drop(df[(df['B0_OWNPV_Y'] < lower_range)].index, inplace=True)
    df.drop(df[(df['B0_OWNPV_Y'] > upper_range)].index, inplace=True)
    df.drop(df[(df['B0_ENDVERTEX_CHI2'] > 30)].index, inplace=True)
    df.drop(df[(df['Pi_ETA'] > 5.23)].index, inplace=True)
def cut_pik(df):
    df.drop(df[(df['Pi_ProbNNp']-df['Pi_ProbNNpi'] > 0.00)&(df['B0_M'] > 5170)&(df['B0_M'] < 5691)].index, inplace = True)
    df.drop(df[(df['Pi_ProbNNk']-df['Pi_ProbNNpi'] > 0.00)&(df['B0_M'] > 5170)&(df['B0_M'] < 5691)].index, inplace = True)
def cut_jpsi(df):
    df.drop(df[(df['Pi_ProbNNmu'] > 0.6)&(df['J_psi_M'] > 540)&(df['J_psi_M'] < 3500)].index, inplace = True)
    df.drop(df[(df['Pi_ProbNNpi'] < 0.2)&(df['J_psi_M'] > 540)&(df['J_psi_M'] < 3500)].index, inplace = True)
    df.drop(df[(df['K_ProbNNk'] < 0.2)&(df['J_psi_M'] > 420)&(df['J_psi_M'] < 4100)].index, inplace = True)
    df.drop(df[(df['K_ProbNNmu'] > 0.6)&(df['J_psi_M'] > 420)&(df['J_psi_M'] < 4100)].index, inplace = True)
def cut_q2(df):
    df.drop(df[(df['q2'] > 0.98)&(df['q2']<1.1)].index, inplace=True)
    df.drop(df[(df['q2'] > 8.0)&(df['q2']<11.0)].index, inplace=True)
    df.drop(df[(df['q2'] > 12.5)&(df['q2']<15)].index, inplace=True)
def filter_events(signal_file, event_file):
    # Load in the signal event file
    data_signal = pd.read_csv(signal_file, dtype="float32", delimiter=",", skiprows=0)
    df_signal = pd.DataFrame(data_signal) #dataframe of signal

    # Select the top 20 important columns
    important_variables = [df_signal.columns[idx] for idx in np.arange(94)]
    df_signal = df_signal[df_signal.columns.intersection(important_variables)]

    # Signal range determination
    min_values_list = []
    max_values_list = []
    for col in important_variables:
        min_values_list.append(min(df_signal[col].values))
        max_values_list.append(max(df_signal[col].values))

    # Remove rows that have values outside of the min/max range for each column
    def remove_outliers(df, min_values_list, max_values_list, important_variables):
        for col, min_value, max_value in zip(important_variables, min_values_list, max_values_list):
            df.drop(df[(df[col] < min_value) | (df[col] > max_value)].index, inplace=True)
        return df
    
    # Event filtering
    event_signal = pd.read_csv(event_file, dtype="float32", delimiter=",", skiprows=0)
    event_signal = pd.DataFrame(event_signal)

    event_signal_cleaned = remove_outliers(event_signal, min_values_list, max_values_list, important_variables)
    return event_signal_cleaned
def filter_events_df (df_signal, event_signal):
    # Select the top 20 important columns
    important_variables = [df_signal.columns[idx] for idx in np.arange(94)]
    df_signal = df_signal[df_signal.columns.intersection(important_variables)]

    # Signal range determination
    min_values_list = []
    max_values_list = []
    for col in important_variables:
        min_values_list.append(min(df_signal[col].values))
        max_values_list.append(max(df_signal[col].values))

    # Remove rows that have values outside of the min/max range for each column
    def remove_outliers(df, min_values_list, max_values_list, important_variables):
        for col, min_value, max_value in zip(important_variables, min_values_list, max_values_list):
            df.drop(df[(df[col] < min_value) | (df[col] > max_value)].index, inplace=True)
        return df
    
    # Event filtering

    event_signal_cleaned = remove_outliers(event_signal, min_values_list, max_values_list, important_variables)
    return event_signal_cleaned
    
def select(df):
    cut_IPCHI2_OWNPV(df)
    cut_PV(df)
    cut_probs (df)
    cut_theta_sep(df)
    cut_DIRA(df)
    cut_K_mass(df)
    cut_FDCHI(df)
    cut_phimumu(df)
    cut_Kmumu(df)
    cut_pik(df)
    cut_jpsi(df)
    cut_q2(df)
    
def filter_light(df_signal, df):
    cut_q2(df)
    cut_IPCHI2_OWNPV(df)
    cut_PV(df)
    cut_probs (df)
    cut_theta_sep(df)
    cut_DIRA(df)
    cut_K_mass(df)
    cut_FDCHI(df)
    filter_events_df (df_signal, df)
    data = laf.likelihood_filter_final(df)
    return data