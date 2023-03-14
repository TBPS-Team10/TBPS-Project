#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 22:19:41 2023

@author: emilyip
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import random
warnings.filterwarnings('ignore')
from GNB_class import *

filenames = ["sig.csv", "jpsi.csv", "Jpsi_Kstarp_pi0.csv", "jpsi_mu_k_swap.csv",
             "jpsi_mu_pi_swap.csv", "k_pi_swap.csv", "Kmumu.csv", "Kstarp_pi0.csv",
             "phimumu.csv", "pKmumu_piTok_kTop.csv", "pKmumu_piTop.csv",
             "psi2s.csv"]
    
#%%
test_df = pd.DataFrame(columns=variables)
train_df = pd.DataFrame(columns=variables)
real_event = []
for i in range(len(filenames)):
    data = pd.read_csv(filenames[i])
    data['event'] = [i]* len(data)
    l = int(len(data)/2)
    test_df=test_df.append(data[:l-1])
    train_df=train_df.append(data[l:])
    real_event.append([i]*(len(data[:l-1])))
    print(i)
#%%
nba = NBA_fit(train_df)
#%%
predictions = predict(df, nba)                                                     
