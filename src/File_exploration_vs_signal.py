#!/usr/bin/env python
# coding: utf-8

# In[ ]:

#Instructions:
#1. Put your file name into the kmumu = [] (on line 24 above signal)
#3. Go to line 89 and change and replace 'Kstarp_pi0' with your filename for the label
#4. Go to line 90 and change and replace 'Kstarp_pi0' with your filename for the set title
#5. Go to line 112 and change and replace 'Kstarp_pi0' with your filename for the label
#6 . Go to line 113 and change and replace 'Kstarp_pi0' with your filename for the set title
#7. Run file and interpret plots
#8. Update the onenote with your results

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize
import scipy
import pandas as pd
from scipy.optimize import curve_fit
from scipy.special import factorial
from scipy.stats import poisson
from scipy.stats import norm
import math


# In[ ]:


kmumu = ["Kstarp_pi0.csv"] # "Kstarp_pi0.csv"
signal = ["sig.csv"]


path = "../data/"  # Uses relative file path, please run from the "src" directory
# Load in the files


# In[ ]:


name_1= kmumu[0]
data_kmumu = pd.read_csv(path+name_1, dtype="float32", delimiter=",", skiprows=0)
df_kmumu = pd.DataFrame(data_kmumu)


# In[ ]:


name_2= signal[0]
data_signal = pd.read_csv(path+name_2, dtype="float32", delimiter=",", skiprows=0)
df_signal = pd.DataFrame(data_signal)
    
    


# In[ ]:


important_variables = []
feauture_columns = [42,43,29,28,46,64,90,93,72,0,32,83,56,48,2,47,51,54,57,65,30,68,92,34,4,82,49,33,37,40]
for idx in feauture_columns:
    important_variables.append(df_signal.columns[idx])
df_signal = df_signal[df_signal.columns.intersection(important_variables)]
df_kmumu = df_kmumu[df_kmumu.columns.intersection(important_variables)]


# In[ ]:


n = 3
n_bins = 100
for col in important_variables:
    
    ##Values specific to datframes
    min_value_1 = min(df_signal[col].values) #Get minimum value 
    max_value_1 = max(df_signal[col].values) #Get maximum value
    bins_1 = np.linspace(min_value_1, max_value_1, n_bins) #Create bins of equal size between min_value and max_value
    min_value_2 = min(df_kmumu[col].values)#Get minimum value 
    max_value_2 = max(df_kmumu[col].values) #Get maximum value of column pairs
    bins_2 = np.linspace(min_value_2, max_value_2, n_bins) #Create bins of equal size between min_value and max_value
    ###
    
    f, (ax1, ax2) = plt.subplots(1, 2, layout ='tight')
    
    ax1.hist(df_signal[col].values, bins=bins_1, alpha=0.5, color='red',label= ('signal: '+col))
    ax1.set_title('signal: '+ str(col))
    
    ax2.hist( df_kmumu[col].values,bins=bins_2, alpha=0.5, color='blue',label=('Kstarp_pi0: '+col))
    ax2.set_title('Kstarp_pi0: '+ str(col))
    


# In[ ]:


n = 3
n_bins = 100
for col in important_variables:
    
    ##Values specific to datframes
    min_value_1 = min(df_signal[col].values) #Get minimum value 
    max_value_1 = max(df_signal[col].values) #Get maximum value
    bins_1 = np.linspace(min_value_1, max_value_1, n_bins) #Create bins of equal size between min_value and max_value
    #
    min_value_2 = min(df_kmumu[col].values)#Get minimum value 
    max_value_2 = max(df_kmumu[col].values) #Get maximum value of column pairs
    bins_2 = np.linspace(min_value_2, max_value_2, n_bins) #Create bins of equal size between min_value and max_value
    
    #Comparison plots
    f, (ax3) = plt.subplots(1, 1, layout ='tight')
    ax3.hist(df_signal[col].values, bins=bins_1, alpha=0.8, color='red',label= ('signal: '+col))
    ax3.hist( df_kmumu[col].values,bins=bins_2, alpha=0.8, color='blue',label=('Kstarp_pi0: '+col))
    ax3.set_title('Signal vs Kstarp_pi0 comparison '+ str(col))
    ax3.legend()


# In[ ]:




