# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 16:06:48 2023

Set the working directory as the folder containing all the .csv sample files.
This script will probably take over an hour to run and may need roughly
1.5 GB of available RAM at peak (the script will crash if it isn't available!).

@author: Madhuwrit Hazra
"""

import numpy as np
import pandas as pd
import model_XGB

filenames = ["sig.csv", "jpsi.csv", "Jpsi_Kstarp_pi0.csv", "jpsi_mu_k_swap.csv",\
             "jpsi_mu_pi_swap.csv", "k_pi_swap.csv", "Kmumu.csv", "Kstarp_pi0.csv",\
             "phimumu.csv", "pKmumu_piTok_kTop.csv", "pKmumu_piTop.csv",\
             "psi2s.csv"]

# Data stored as 32-bit floats to save RAM. ML processes everything in 32-bit, anyway.
# Your PC will suffer extreme paralysis if you try to use 64-bit with insufficient RAM!

# Split into a training dataset
X_train = []
y_train = []

# Split into a testing dataset
X_test = []
y_test_true = []  # Actual values; used for testing accuracy

# Load in the files
for i, name in enumerate(filenames):
    # Load as float32 to save RAM
    data = np.loadtxt("./data/" + name, dtype="float32", delimiter=",", skiprows=1)
    samples = len(data)
    X_train.append(data[:samples//2])
    y_train.append(np.ones(samples//2).astype("int32") * i)
    X_test.append(data[samples//2:])
    y_test_true.append(np.ones(samples - samples//2).astype("int32") * i)
    
del data  # Free up some RAM (can be significant)

# Literally take one (the smallest one) just to get a list of variable names
# if you need them
variables = pd.read_csv("./data/jpsi_mu_pi_swap.csv")
variables = list(variables.columns)

# Combine into 32-bit arrays for use in ML
X_train = np.concatenate(X_train).astype("float32")
y_train = np.concatenate(y_train).astype("int32")
X_test = np.concatenate(X_test).astype("float32")
# The model will predict the values of y_test and compare to y_test_true to measure accuracy
y_test_true = np.concatenate(y_test_true).astype("int32")

#%% Fit the model and test the data

bdt_model = model_XGB.BDT_model(max_depth=3, n_estimators=200, num_features=30)
bdt_model.feature_selection_ANOVA(X_train, y_train)
bdt_model.fit(X_train, y_train)
y_test = bdt_model.predict(X_test)

accuracy = 100. * np.sum(y_test == y_test_true) / len(y_test_true)
# 44961 B0 decay events are known
# This is essentially the true positive rate/percentage
B0_accuracy = 100. * np.sum(y_test[:44961] == y_test_true[:44961]) / 44961
print("Model accuracy on testing data = %.2f percent" % (accuracy))
print("B0 event accuracy = %.2f percent" % (B0_accuracy))

# Save the model for use elsewhere; change the name to whatever is needed.
# Don't overwrite models you don't want to lose!
bdt_model.save_model("model_depth_3_estimators_200_features_10.json")