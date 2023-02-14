#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 16:53:10 2023

@author: Avi
"""

#!/usr/bin/env python
# coding: utf-8   

#%%
'''
To use this function:-

filtered_events = filter_events(sig.csv filepath, investigated event filepath)
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def filter_events(signal_file, event_file):
    # Load in the signal event file
    data_signal = pd.read_csv(signal_file, dtype="float32", delimiter=",", skiprows=0)
    df_signal = pd.DataFrame(data_signal) #dataframe of signal

    # Select the top 20 important columns
    important_variables = [df_signal.columns[idx] for idx in [42, 43, 29, 28, 46, 64, 90, 93, 72, 0, 32, 83, 56, 48, 2, 47, 51, 54, 57, 65]]
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
    
    def other_filters(df):
        df.drop(df[(df['B0_OWNPV_Y'] < -0.27)&(df['B0_OWNPV_Y'] > -0.09)].index, inplace = True)
        #df.drop(df[(df['B0_M'] < 5220)&(df['B0_M'] > 5340)].index, inplace = True)
        df.drop(df[(df['B0_ENDVERTEX_CHI2'] < 11)].index, inplace = True)
        df.drop(df[(df['Kstar_ENDVERTEX_CHI2'] < 2)].index, inplace = True)
        #df.drop(df[(df['Kstar_PT'] < 9500)].index, inplace = True)
        df.drop(df[(df['B0_OWNPV_X'] < 0.75)&(df['B0_OWNPV_X'] > 0.93)].index, inplace = True)

    # Event filtering
    event_signal = pd.read_csv(event_file, dtype="float32", delimiter=",", skiprows=0)
    event_signal = pd.DataFrame(event_signal)

    print(event_signal) #dataframe before filtering
    event_signal_cleaned = remove_outliers(event_signal, min_values_list, max_values_list, important_variables)
    print(event_signal) #dataframe after filtering
    event_signal_further_cleaned = other_filters(event_signal_cleaned)
    print(event_signal)
    return event_signal_further_cleaned

#%%
#test
#filtered_data = filter_events("../data/sig.csv","../data/total_dataset.csv")