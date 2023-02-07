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
    def __init__(self, max_depth=3, n_estimators=200, num_features=30):
        """
        Boosted decision tree ML model built with XGBoostClassifier(). Default
        parameters are set to the ones used to train the provided .json file
        for a ready, trained ML model.

        Parameters
        ----------
        max_depth : int, optional
            Max BDT tree depth. The default is 3.
        n_estimators : int, optional
            Max boosting iterations. The default is 200.
        num_features : int, optional
            Number of top features to select (recommend no higher than 30).
            The default is 30.

        Returns
        -------
        None.

        """
        self._max_depth = max_depth
        self._n_estimators = n_estimators
        self._num_features = num_features
        
    def feature_selection_ANOVA(self, X_train, y_train):
        """
        Performs the ANOVA feature selection algorithm and stores resultant
        F scores in the BDT_model object as BDT_model._F_scores.

        Parameters
        ----------
        X_train : ndarray
            Training data.
        y_train : ndarray
            Training targets (categorical).

        Returns
        -------
        None.

        """
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
            
    def specify_feature_num(self, num_features):
        """
        If you load an external model from a .json, you need to tell it how many
        features to select. This is a result of not being able to save the entire
        BDT_model class object, but only the XGBoostClassifier object (i.e. the
        actual model).

        Parameters
        ----------
        num_features : int
            The number of features selected for the algorithm.

        Returns
        -------
        None.

        """
        self._num_features = num_features
        
    def specify_features(self, feature_indices):
        """
        If you load an external .json model, you need to tell it the indices
        of the variables you want it to select; the total number should
        match the number of features you want the model to select—specify this with
        BDT_model.specify_feature_num(). This is a consequence only being able to
        save the XGBoostClassifier model object, not the whole BDT_model class.

        Parameters
        ----------
        feature_indices : list/ndarray of ints
            Indices (0-93) of the features you want to select for the algorithm.

        Returns
        -------
        None.

        """
        self._best_features = feature_indices[:self._num_features]
        
    def plot_F_scores(self):
        """
        Plots F scores in a bar plot after feature selection (for investigative
        purposes).

        Returns
        -------
        None.

        """
        # For investigative purposes and debugging
        plt.bar([i for i in range(len(self._F_scores))], self._F_scores)
        plt.show()
        
    def fit(self, X_train, y_train):
        """
        Trains the model against a testing dataset, X_train, and a target dataset,
        y_train.

        Parameters
        ----------
        X_train : ndarray
            Training dataset (all variables; the function will cut it down to the
            selected features automatically).
        y_train : ndarray
            Target dataset (classifications from 0 to 11).

        Returns
        -------
        None.

        """
        # Reduce X_train down to the best features
        X_train_selected = X_train[:,self._best_features]
        # Define XGBoost classification object
        self._bdt = xgboost.XGBClassifier(max_depth=self._max_depth, n_estimators=self._n_estimators)
        self._bdt.fit(X_train_selected, y_train)
        
    def predict(self, X_test):
        """
        Predicts classification outputs (0 to 11) based on input dataset, X_test,
        with all features. The function will automatically cut X_test down to
        the selected features.

        Parameters
        ----------
        X_test : ndarray
            Testing dataset.

        Returns
        -------
        y_test : ndarray
            Classification predictions based on testing dataset, X_test.

        """
        X_test_selected = X_test[:,self._best_features]
        self._y_test = self._bdt.predict(X_test_selected)
        
        return self._y_test
    
    def predict_proba(self, X_test):
        """
        Predicts classification probabilities (i.e. confidence in results) of
        classifications of X_test. 12 columns will be returned, corresponding to
        the probability of each decay event (each row) being each of the 12 trained
        decay types. Many are likely to be >99% confident, even if it is not
        always correct! This is a result of how BDT ML algorithms work.

        Parameters
        ----------
        X_test : ndarray
            Testing dataset.

        Returns
        -------
        Probabilities : ndarray
            Prediction probabilities of each class for each decay event/row.

        """
        X_test_selected = X_test[:,self._best_features]
        return self._bdt.predict_proba(X_test_selected)
    
    def save_model(self, filename):
        """
        Saves the current XGBoostClassifier object as a .json file. This will not
        save the number of selected features and what features in particular it selected;
        these need to be specified again if the model is loaded!

        Parameters
        ----------
        filename : string
            File name to save model as.

        Returns
        -------
        None.

        """
        self._bdt.save_model(filename)
        
    def load_model(self, filename):
        """
        Loads a saved XGBoostClassifier model into the BDT_model class object.
        You will need to specify the number of features and the particular selected
        features again! For the model I have provided, there is an accompanying
        text file with a list of the needed features for that particular algorithm.

        Parameters
        ----------
        filename : 
            File name of .json model to load.

        Returns
        -------
        None.

        """
        self._bdt = xgboost.XGBClassifier()
        self._bdt.load_model(filename)
