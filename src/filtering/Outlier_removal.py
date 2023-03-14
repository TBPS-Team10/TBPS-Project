#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 16:53:10 2023

@author: Avi
"""

#!/usr/bin/env python
# coding: utf-8   

#%% Range calculation for sig.csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load in the signal event file
signal_file = "../data/sig.csv"
data_signal = pd.read_csv(signal_file, dtype="float32", delimiter=",", skiprows=0)
df_signal = pd.DataFrame(data_signal) #dataframe of signal

# Select the top 20 important columns
important_variables = [df_signal.columns[idx] for idx in [42, 43, 29, 28, 46, 64, 90, 93, 72, 0, 32, 83, 56, 48, 2, 47, 51, 54, 57, 65]]
df_signal = df_signal[df_signal.columns.intersection(important_variables)]

min_values_list = []
max_values_list = []
for col in important_variables:
    min_values_list.append(min(df_signal[col].values))
    max_values_list.append(max(df_signal[col].values))
#%% Outlier removal function

# Remove rows that have values outside of the min/max range for each column
def remove_outliers(df, min_values_list, max_values_list, important_variables):
    for col, min_value, max_value in zip(important_variables, min_values_list, max_values_list):
        df.drop(df[(df[col] < min_value) | (df[col] > max_value)].index, inplace=True)
    return df
#%% Event filtering

event_file = "../data/jpsi_mu_k_swap.csv" #change the event filename as required
event_signal = pd.read_csv(event_file, dtype="float32", delimiter=",", skiprows=0)
event_signal = pd.DataFrame(event_signal)

print(event_signal) #dataframe before filtering
event_signal_cleaned = remove_outliers(event_signal, min_values_list, max_values_list, important_variables)
print(event_signal_cleaned) #dataframe after filtering