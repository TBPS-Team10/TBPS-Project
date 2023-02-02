#!/usr/bin/env python
# coding: utf-8

# In[6]:


# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 19:04:34 2023

@author: Regen Petu-Stiles
"""

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




filenames = ["Kmumu.csv"] # "Kstarp_pi0.csv"


path = r"C:/Users/Toshiba/Desktop/Regen/TBPS/TBPS - Spring 2023/Data/"  # please change to your own filepath  
# Load in the files


# In[ ]:





# In[2]:


###poisson exploration function
def poisson_exploration(data):

    # the bins should be of integer width, because poisson is an integer distribution
    bins = 1000
    entries, bin_edges, patches = plt.hist(data, bins=bins, density=True, label='Data')
    plt.xlabel(col+ ' Values')
    plt.ylabel('Normalised Frequency')

    # calculate bin centers
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])


    def fit_function(k, lamb):
        '''poisson function, parameter lamb is the fit parameter'''
        return scipy.stats.poisson.pmf(k, lamb)


    # fit with curve_fit
    parameters, cov_matrix = curve_fit(fit_function, bin_centers, entries)

    # plot poisson-deviation with fitted parameter
    x_plot = np.arange(min(data), max(data))

    plt.plot(
        x_plot,
        fit_function(x_plot, *parameters),
        marker='o', linestyle='',
        label='Fit result'
    )
    plt.legend()
    plt.show()
    import scipy.optimize as optimize


    def poisson(k, lamb):
        #"""poisson pdf, parameter lamb is the fit parameter"""
        return (lamb**k/factorial(k)) * np.exp(-lamb)

    def negative_log_likelihood(params, data):
        """
        The negative log-Likelihood-Function
        """
        lnl = - np.sum(np.log(poisson(data, params[0])))
        return lnl


    # minimize the negative log-Likelihood

    result = optimize.minimize(negative_log_likelihood,  # function to minimize
                      x0=parameters[0],            # start value
                      args=(data),             # additional arguments for function
                      method='Powell',          # minimization method, see docs
                      )
    # result is a scipy optimize result object, the fit parameters 
    # are stored in result.x
    print(result)
    print( "Poisson fit parameters"   +  str(result.x))
    return 
    #


# In[3]:


#Gaussian exploration function:
def gaussian_exploration(data):


    # Fit a normal distribution to the data:
    mu, std = norm.fit(data)

    # Plot the histogram.
    h, xedges, patches=plt.hist(data, bins=25, density=True, alpha=0.6, color='g')
    
    #find bin centres
    xcenters = np.mean(np.vstack([xedges[:-1], xedges[1:]]), axis=0)
    
    # Plot the PDF.
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax+4, 100)
    p = norm.pdf(x-2.5, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    column_name = col
    title = "Fit results for " + column_name +": mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title)
    plt.xlabel(col+ ' Values')
    plt.ylabel('Normalised Frequency')
    plt.show()
    
    #log likelihood estimation
    def llnorm(par, data):
        n = len(data)
        mu, sigma = par
        ll = np.sum(math.log(2*math.pi*(sigma**2))/2 + ((data-mu)**2)/(2 * (sigma**2)))
        return ll

    result = optimize.minimize(llnorm, [mu,std], args = (data))
    print(result)
    print( "Guassian fit parameters"   +  str(result.x))


# In[4]:


###Example below


# In[7]:


#manual reading in of data
kmumu_data = pd.read_csv(r"Data/Kmumu.csv", on_bad_lines='skip')

col ='q2'
# get data
data = kmumu_data[col]

poisson_exploration(data)#calling poisson exploration function
gaussian_exploration(data)#calling Gaussian exploration function


# In[ ]:


#Automated


# In[ ]:


#takes some time to run- 
#would be best to input the 20 or so columns 
#that we know are important instead of all columns(variables)
for name in filenames:
    data = pd.read_csv(path+name, dtype="float32", delimiter=",", skiprows=0)
    df = pd.DataFrame(data)
    
   

for col in df.columns:
    try:
        poisson_exploration(data)#calling poisson exploration function
    except:
        print('Poisson fit failed for column: ' +col)
        
    try:
        gaussian_exploration(data)#calling Gaussian exploration function
    except:
        print('Gaussian fit failed for column: ' +col)
        


# In[ ]:




