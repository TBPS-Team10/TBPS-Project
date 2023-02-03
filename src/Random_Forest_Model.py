#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
Created on Wed Jan 25 2023

Descrpition : Random Forest classifier for decay events.

@author: Regen Petu-Stiles
"""
# Model RF
import numpy as np
import seaborn as sns
from sklearn.feature_selection import f_classif
from sklearn.feature_selection import SelectKBest
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt


class Random_Forest_Model:
    def __init__(self, n_estimators=50, max_features=20):
        self._n_estimators = n_estimators
        self._num_features = max_features

    # input the models feature selection criteria # Same as before
    def feature_selection_ANOVA_RF(self, X_train, y_train):
        # Select all features for now and see how they correlate to the output
        self._fs = SelectKBest(score_func=f_classif, k="all")
        # Find a relationship between the training data and its outputs
        self._fs.fit(X_train, y_train)
        self._F_scores = self._fs.scores_
        # Replace negative or NaN F scores with 0, then select best features
        self._F_scores = np.where(self._F_scores > 0, self._F_scores, 0.)
        self._best_features = np.argsort(self._F_scores)[::-1][:self._num_features]

        # Print F scores
        for i in range(len(self._F_scores)):
            print('Feature %i: %f' % (i, self._F_scores[i]))

    def plot_F_scores_RF(self):
        # Creating a bar plot
        sns.barplot([i for i in range(len(self._F_scores))], self._F_scores)
        # Add labels to your graph
        plt.xlabel('Feature Importance Score')
        plt.ylabel('Features')
        plt.title("Visualizing Important Features")
        plt.legend()
        plt.show()

    def fit(self, X_train, y_train):
        # Reduce X_train down to the best features
        X_train_selected = X_train[:, self._best_features]
        # Define Random Forest classification object
        self._RF = RandomForestClassifier(n_estimators=self._n_estimators)
        self._RF.fit(X_train_selected, y_train)

    def predict(self, X_test):
        X_test_selected = X_test[:, self._best_features]
        self._y_test = self._RF.predict(X_test_selected)

        return self._y_test


# In[2]:


# -*- coding: utf-8 -*-
"""
Created on Thurs Jan 25 2023

Note:
Working directory = your decay data folder (folder with 'sig.csv'... etc).


@author: Regen Petu-Stiles 
"""

# Main_RF
from sklearn.ensemble import RandomForestClassifier
# Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics
import numpy as np
import pandas as pd
import sklearn as sk
from pathlib import Path
import joblib  # to save RF model
import pickle

filenames = ["sig.csv", "jpsi.csv", "Jpsi_Kstarp_pi0.csv", "jpsi_mu_k_swap.csv", "jpsi_mu_pi_swap.csv", "k_pi_swap.csv",
             "Kmumu.csv", "Kstarp_pi0.csv", "phimumu.csv", "pKmumu_piTok_kTop.csv", "pKmumu_piTop.csv", "psi2s.csv", ]

# Split into a training dataset
X_train = []
y_train = []

# Split into a testing dataset
X_test = []
y_test_true = []  # Actual values; used for testing accuracy

path = r"Data/"  # change to "../data/" before pushing
# Load in the files
for i, name in enumerate(filenames):
    data = np.loadtxt(path + name, dtype="float32", delimiter=",", skiprows=1)
    samples = len(data)
    X_train.append(data[:samples // 2])
    y_train.append(np.ones(samples // 2).astype("int32") * i)
    X_test.append(data[samples // 2:])
    y_test_true.append(np.ones(samples - samples // 2).astype("int32") * i)

del data  # Free up some RAM (can be significant)

# Literally take one (the smallest one) just to get a list of variable names
# if you need them
variables = pd.read_csv(path + "jpsi_mu_pi_swap.csv")
variables = list(variables.columns)

# Combine into 32-bit arrays for use in ML
X_train = np.concatenate(X_train).astype("float32")
y_train = np.concatenate(y_train).astype("int32")
X_test = np.concatenate(X_test).astype("float32")
# The model will predict the values of y_test and compare to y_test_true to measure accuracy
y_test_true = np.concatenate(y_test_true).astype("int32")

# %% Fit the model and test the data

# rf_model = model_RF.Random_Forest_Model( n_estimators=200, num_features=20)
rf_model = Random_Forest_Model(n_estimators=200, max_features=20)
rf_model.feature_selection_ANOVA_RF(X_train, y_train)
rf_model.fit(X_train, y_train)
y_test = rf_model.predict(X_test)

accuracy = 100. * np.sum(y_test == y_test_true) / len(y_test_true)
# 44961 B0 decay events are known
B0_accuracy = 100. * np.sum(y_test[:44961] == y_test_true[:44961]) / 44961
print("Model accuracy on testing data = %.2f percent" % (accuracy))
print("B0 event accuracy = %.2f percent" % (B0_accuracy))

# Save the model
# Change the name
# Be careful not to overwrite models you don't want to lose!

# save
pckl_filename = "random_forest_model.pkl"
joblib.dump(rf_model, pckl_filename)

# In[3]:


# rf_model = model_RF.Random_Forest_Model( n_estimators=200, num_features=20)


# In[ ]:


# In[24]:


####Load model from file####
# rf_classifer = joblib.load("random_forest_model.pkl")


# In[25]:


####USE IT TO MAKE PREDICTIONS ####


# In[26]:


#### Create new observation####
# new_observation = input your data here

####Predict observation's class####
# rf_classifer.predict(new_observation)


# In[ ]:


# In[27]:


###Model Interpretation


# In[28]:


###we can actually examine any of the trees in the forest.
# We will select one tree, and save the whole tree as an image.


# In[29]:


# Import tools needed for visualization
from sklearn.tree import export_graphviz
# !pip install pydot
import pydot

# or
# from sklearn import tree
# tree.plot_tree(rf_model._best_estimator_.estimators_[k])


# In[30]:


"""
# Pull out one tree from the forest
tree = rf_model._n_estimators

# Export the image to a dot file
export_graphviz(tree, out_file = 'tree.dot', feature_names = feature_list, rounded = True, precision = 1)
# Use dot file to create a graph
(graph, ) = pydot.graph_from_dot_file('tree.dot')
# Write graph to a png file
graph.write_png('tree.png')
"""
