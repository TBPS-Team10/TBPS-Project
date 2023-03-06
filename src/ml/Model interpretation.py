#!/usr/bin/env python
# coding: utf-8

# In[38]:



import xgboost as xgb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import model_XGB
import eli5
from eli5 import show_prediction, show_weights
import graphviz
from graphviz import Digraph
from xgboost import plot_tree



# In[27]:



#extracts the feautures as column numbers and as names
#If you have a prexisting method that does this AND preserves the column order, please feel free to replace
path = #####replace with the path to your data####

signal = ["sig.csv"]
name_2= signal[0]
data_signal = pd.read_csv(path+name_2, dtype="float32", delimiter=",", skiprows=0)
df_signal = pd.DataFrame(data_signal)
important_variables = []

feauture_columns = [56,57,93,65,48,42,49,83,47,51,54,43,68,46,60,90,80,72,76,55]
for idx in feauture_columns:
    important_variables.append(df_signal.columns[idx])
df_signal = df_signal[df_signal.columns.intersection(important_variables)]
feautures = df_signal.columns
feautures= feautures.tolist()


# In[28]:


feature_list=feauture_columns

bdt_model=model_XGB.BDT_model()
bdt_model.load_model("model_depth_3_estimators_200_features_20.json")
bdt_model.specify_feature_num(20)
bdt_model.specify_features(feature_list)
model=bdt_model


# In[ ]:


# the below may need to be uncommented and used instead of loading in the model from the class above.
#To visualise the BDT I need access to methoda inside XGBoost that have not been
#carried forward into the ML class we are using for this project. 
"""
# These filenames specify the order of the classification from 0 to 11—important!
filenames = ["sig.csv", "jpsi.csv", "Jpsi_Kstarp_pi0.csv", "jpsi_mu_k_swap.csv",
             "jpsi_mu_pi_swap.csv", "k_pi_swap.csv", "Kmumu.csv", "Kstarp_pi0.csv",
             "phimumu.csv", "pKmumu_piTok_kTop.csv", "pKmumu_piTop.csv",
             "psi2s.csv"]

# Data stored as 32-bit floats to save RAM. ML processes everything in 32-bit, anyway.
# Your PC will suffer extreme paralysis if you try to use 64-bit with insufficient RAM!

# Split into a training dataset
X_train = []
y_train = []

# Split into a testing dataset
X_test = []
y_test_true = []  
# Actual values; used for testing accuracy
features= loadtxt(r"C:\Users\Toshiba\Documents\GitHub\TBPS-Project\src\ml\post_filter_ML_20_features.csv", delimiter=",", dtype="int32")
features
# Load in the files
path =r"C:/Users/Toshiba/Documents/GitHub/TBPS-Project/data/"
for i, name in enumerate(filenames):
    if i==0:
        # Load as float32 to save RAM
        data = np.loadtxt(path + name, dtype="float32", delimiter=",", skiprows=1)
        data = data[:,features]
        samples = len(data)
        X_train.append(data[:samples//2])
        y_train.append(np.ones(samples//2).astype("int32") * i)
        X_test.append(data[samples//2:])
        y_test_true.append(np.ones(samples - samples//2).astype("int32") * i)
    else:
        data = np.loadtxt(path + name, dtype="float32", delimiter=",", skiprows=1)
        data = data[:,features]
        samples = len(data)
        X_train.append(data[:samples//2])
        y_train.append(np.ones(samples//2).astype("int32") * 1)
        X_test.append(data[samples//2:])
        y_test_true.append(np.ones(samples - samples//2).astype("int32") * 1)
    
    
del data  # Free up some RAM (can be significant)



# Combine into 32-bit arrays for use in ML
X_train = np.concatenate(X_train).astype("float32")
y_train = np.concatenate(y_train).astype("int32")
X_test = np.concatenate(X_test).astype("float32")
# The model will predict the values of y_test and compare to y_test_true to measure accuracy
y_test_true = np.concatenate(y_test_true).astype("int32")



model = XGBClassifier( max_depth=3, n_estimators=200, num_features=30)
model.fit(X_train, y_train)
y_test = model.predict(X_test)

accuracy = 100. * np.sum(y_test == y_test_true) / len(y_test_true)
# 44961 B0 decay events are known
# This is essentially the true positive rate/percentage
B0_accuracy = 100. * np.sum(y_test[:44961] == y_test_true[:44961]) / 44961
print("Model accuracy on testing data = %.2f percent" % (accuracy))
print("B0 event accuracy = %.2f percent" % (B0_accuracy))

"""


# In[39]:


plot_tree(model)


# In[ ]:


plot_tree(model, num_trees=7, rankdir='LR')


# In[33]:


df = model.get_booster().trees_to_dataframe()
df = df[df['Yes'].notna()]
df.set_index('Feature',inplace= True)
new_df =df.T
new_df
unique_columns= new_df.columns.unique()


# In[ ]:


#creating a way to map columns to column numbers in the simplified BDT 


# In[34]:


assignment=[unique_columns.tolist(),feauture_columns,feautures]
assignment= pd.DataFrame(assignment)
tree_index= assignment.T[0]
model_training_index= assignment.T[1]
column_assignment =assignment.T[2]
text_model_rules =  model.get_booster().get_dump()
 
for num in range(len(text_model_rules)):
    
    for i, feat_num in enumerate(tree_index):
        #print(text_model_rules[num])
        re.sub(tree_index[i],column_assignment[i],text_model_rules[num])
for i, feat_num in enumerate(tree_index):
    print(text_model_rules[1])


# In[35]:


show_weights(model, feature_names=feautures,
             show=["feature_importances"])


# In[36]:


show_weights(model, feature_names=feautures,
             show=["decision_tree", "method", "description"])#visually showing the importance of featuures


# In[37]:


#The below code reads the dump file created by xgboost and writes a scoring code in SAS:

import re
def string_parser(s):
    if len(re.findall(r":leaf=", s)) == 0:
        out  = re.findall(r"[\w.-]+", s)
        tabs = re.findall(r"[\t]+", s)
        if (out[4] == out[8]):
            missing_value_handling = (" or missing(" + out[1] + ")")
        else:
            missing_value_handling = ""

        if len(tabs) > 0:
            return (re.findall(r"[\t]+", s)[0].replace('\t', '    ') + 
                    '        if state = ' + out[0] + ' then do;\n' +
                    re.findall(r"[\t]+", s)[0].replace('\t', '    ') +
                    '            if ' + out[1] + ' < ' + out[2] + missing_value_handling +
                    ' then state = ' + out[4] + ';' +  ' else state = ' + out[6] + ';\nend;' ) 
        else:
            return ('        if state = ' + out[0] + ' then do;\n' +
                    '            if ' + out[1] + ' < ' + out[2] + missing_value_handling +
                    ' then state = ' + out[4] + ';' +  ' else state = ' + out[6] + ';\nend;' )
    else:
        out = re.findall(r"[\w.-]+", s)
        return (re.findall(r"[\t]+", s)[0].replace('\t', '    ') + 
                '        if state = ' + out[0] + ' then\n    ' +
                re.findall(r"[\t]+", s)[0].replace('\t', '    ') + 
                '        value = value + (' + out[2] + ') ;\n')

def tree_parser(tree, i):
    return ('state = 0;\n'
             + "".join([string_parser(tree.split('\n')[i]) for i in range(len(tree.split('\n'))-1)]))

def model_to_sas(model, out_file):
    trees= model.get_booster().get_dump()
    
    result = ["value = 0;\n"]
    with open(out_file, 'w') as the_file:
        for i in range(len(trees)):
            result.append(tree_parser(trees[i], i))
        the_file.write("".join(result))
        the_file.write("\nY_Pred1 = 1/(1+exp(-value));\n")
        the_file.write("Y_Pred0 = 1 - Y_pred1;") 


# In[ ]:


model_to_sas(model, 'xgb_scr_code.sas')#creating text file


# In[ ]:


model.get_booster().feature_names#checking feauture names have been replaced

