# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 02:48:35 2023

XGBoost BDT classifier for decay events.
                               
Have patience—fitting a model to over 1,000,000 samples takes time.

@author: Madhuwrit Hazra
"""

import numpy as np
import matplotlib.pyplot as plt
import xgboost
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif  # ANOVA feature selection algorithm

class BDT_model:
    def __init__(self, max_depth=3, n_estimators=200, num_features=20):
        self._max_depth = max_depth
        self._n_estimators = n_estimators
        self._num_features = num_features
        
    def feature_selection_ANOVA(self, X_train, y_train):
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
        
    def plot_F_scores(self):
        plt.bar([i for i in range(len(self._F_scores))], self._F_scores)
        plt.show()
        
    def fit(self, X_train, y_train):
        # Reduce X_train down to the best features
        X_train_selected = X_train[:,self._best_features]
        # Define XGBoost classification object
        self._bdt = xgboost.XGBClassifier(max_depth=self._max_depth, n_estimators=self._n_estimators)
        self._bdt.fit(X_train_selected, y_train)
        
    def predict(self, X_test):
        X_test_selected = X_test[:,self._best_features]
        self._y_test = self._bdt.predict(X_test_selected)
        
        return self._y_test
    
    def predict_proba(self, X_test):
        X_test_selected = X_test[:,self._best_features]
        return self._bdt.predict_proba(X_test_selected)
    
    def save_model(self, filename):
        self._bdt.save_model(filename)
        
    def load_model(self, model_name):
        self._bdt = xgboost.XGBClassifier()
        self._bdt.load_model(model_name)