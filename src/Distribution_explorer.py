#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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




filenames = ["Sig.csv"] # "Kstarp_pi0.csv"


path = r"Data/"  # please change to your own filepath  
# Load in the files


# In[ ]:


###poisson exploration function
def poisson_exploration(data,col):
    
    ##Values specific to datframes
   
    n_bins = 1000
    min_value_1 = min(data[col]) #Get minimum value 
    max_value_1 = max(data[col]) #Get maximum value
    bins_1 = np.linspace(min_value_1, max_value_1, n_bins) #Create bins of equal size between min_value and max_value
    #



    # the bins should be of integer width, because poisson is an integer distribution
    #bins = 1000
    entries, bin_edges, patches = plt.hist(data[col], bins=bins_1, density=True, label='Data')
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
    x_plot = np.arange(min(data[col]), max(data[col]))

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
        lnl = - np.sum(np.log(poisson(data[col], params[0])))
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
    print( "Poisson fit parameters "   +  str(result.x))
    print(col)
    return 
    #






# In[ ]:


#Gaussian exploration function:
def gaussian_exploration(data,col):

    #Values specific to column
    n_bins = 1000
    min_value_1 = min(data[col]) #Get minimum value 
    max_value_1 = max(data[col]) #Get maximum value
    bins_2 = np.linspace(min_value_1, max_value_1, n_bins) #Create bins of equal size between min_value and max_value
    #

    # Fit a normal distribution to the data:
    mu, std = norm.fit(data[col])

    # Plot the histogram.
    h, xedges, patches=plt.hist(data[col], bins=bins_2, density=True, alpha=0.6, color='g')
    
    #find bin centres
    xcenters = np.mean(np.vstack([xedges[:-1], xedges[1:]]), axis=0)
    
    # Plot the PDF.
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
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
        ll = np.sum(math.log(2*math.pi*(sigma**2))/2 + ((data[col]-mu)**2)/(2 * (sigma**2)))
        return ll

    result = optimize.minimize(llnorm, [mu,std], args = (data))
    print(result)
    print( "Guassian fit parameters"   +  str(result.x))
    print(col)


# In[ ]:


#Exponetial exploration function:
def exponetial_exploration(data,col):

    size = 300000
    nbins = 50

    ydata = data[col] 

    ## creating the normalized log binned histogram data
    bins = 10 ** np.linspace(np.log10(np.min(ydata)), np.log10(np.max(ydata)), nbins)
    counts, bin_edges = np.histogram(ydata, bins=bins)
    bin_centres = (bin_edges[:-1] + bin_edges[1:]) / 2
    bin_width = (bin_edges[1:] - bin_edges[:-1])
    counts = counts / bin_width / np.sum(counts)

    ## generating arbitrary x value
    x1 = np.linspace(bin_centres.min(), bin_centres.max(), len(ydata))

    def MLE(params):
        """ find the max likelihood """
        k1 = params
        yPred = k1*np.exp(-k1*ydata) 
        negLL = -np.sum(np.log(yPred))
        return negLL

    guess = np.array([1/30])
    ## best function used for global fitting

    result = optimize.minimize(MLE, guess)
    
    K1 = result.x
    
    y_fitted = K1*np.exp(-K1*x1)

    ## plot actual data
    plt.plot(bin_centres, counts, 'ko', label=" actual data",color= 'blue')
    #plt.hist(ydata2)
    plt.xlabel(col + ' Value')
    plt.ylabel("Frequency")

    ## plot fitted data on original data
    plt.plot(x1, y_fitted, c='r', linestyle='dashed', label="fit")
    plt.legend()
    #plt.xscale('log')
    #plt.yscale('log')

    plt.show()
    print(result)
    print(result.x)
    print( "Exponetial fit parameters"   +  str(result.x))
    print(col)


# In[ ]:


###Example below


# In[ ]:


#manual reading in of data
kmumu_data = pd.read_csv(r"Data/Kmumu.csv", on_bad_lines='skip')

test_col ='q2'
# get data
test_data = kmumu_data

poisson_exploration(test_data,test_col)#calling poisson exploration function
gaussian_exploration(test_data,test_col)#calling Gaussian exploration function
exponetial_exploration(test_data,test_col)



# In[ ]:




#takes some time to run- 
#would be best to input the 20 or so columns 
#that we know are important instead of all columns(variables)
for name in filenames:
    df = pd.read_csv(path+name, dtype="float32", delimiter=",", skiprows=0)
    
#Emily's txt copy and pasted here- would be better to automate the reading in of the values
#in case the txt changes
important_variables = []
feauture_columns = [42,43,29,28,46,64,90,93,72,0,32,83,56,48,2,47,51,54,57,65,30,68,92,34,4,82,49,33,37,40]
for idx in feauture_columns:
    important_variables.append(df.columns[idx])
df = df[df.columns.intersection(important_variables)]


# In[ ]:


for col in df.columns:
    try:
        poisson_exploration(df,col)#calling poisson exploration function
    except:
        print('Poisson fit failed for column: ' +col)
        
    try:
        gaussian_exploration(df,col)#calling Gaussian exploration function
    except:
        print('Gaussian fit failed for column: ' +col)
        
    try:
        exponetial_exploration(df,col)
    except:
        print('Exponential fit failed for column: ' +col)


# In[ ]:








