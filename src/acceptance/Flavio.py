#!/usr/bin/env python
# coding: utf-8
#Author: Regen Petu-Stiles
#Date created: March 2023

# Flavio" is a Python package used for computing observables 
# This is a basic notebook so anyone in the team can easily understand what we are doing.
# 
# It provides a set of tools for computing theoretical predictions for various flavor observables, such as: branching ratios, decay rates, mixing angles, and CP-violating phases.
# These observables are important for testing the validity of the Standard Model and for searching for new physics beyond it, in our data

# In[1]:


##install flavio
#!pip install flavio


# In[2]:


import flavio
import unittest
import flavio
from flavio.physics.taudecays import taulnunu
from wilson import Wilson
from math import sqrt
import flavio
import flavio.plots
import flavio.statistics.likelihood
import matplotlib.pyplot as plt
from collections import OrderedDict
import flavio.physics.mesonmixing.wilsoncoefficient as wilson_coefficients
import unittest
import numpy as np
from flavio.physics.mesonmixing import amplitude, observables
from math import sin, asin, cos, pi
from flavio.physics.eft import WilsonCoefficients
from flavio import Observable
from flavio.parameters import default_parameters
import copy
import flavio
import cmath
from wilson import Wilson
from flavio.parameters import default_parameters
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)


# # Checking the form of Wilson Coefficients

# Define the observable you want to study using the Flavio Observable class. For example, if you want to study the CP asymmetry in the decay B0 -> K0 pi0, you could define the observable as follows:
# 
# 

# To calculate the Wilson coefficients from angular observables in bins of q2, you can use the wilsoncoefficients.wilson_coefficients function. Example below

# In[ ]:





# In[3]:


flavio.physics.mesonmixing.observables.Observable('ACP(B0->K0pi0)')


# In[4]:




s = 1.519267515435317e+24

c = copy.deepcopy(default_parameters)
par = c.get_central_all()

wc_obj = WilsonCoefficients()
wc_B0 = wc_obj.get_wc('bdbd', 4.2, par)
CVSM = flavio.physics.mesonmixing.wilsoncoefficient.cvll_d(par, 'B0', scale=80)[0]
w = Wilson({'CVRR_bdbd': CVSM}, 80, 'WET', 'flavio')
flavio.np_prediction('DeltaM_d', w) / flavio.sm_prediction('DeltaM_d')


# In[5]:


wc_B0 = wc_obj.get_wc('bdbd', 4.2, par)
wc_B0


# In[6]:


par


# In[7]:


CVSM = flavio.physics.mesonmixing.wilsoncoefficient.cvll_d(par, 'B0', scale=80)[0]
CVSM


# # Building a statistical test

# In[8]:


SM_parameter_errors= np.loadtxt("SM_parameters_errors.csv", delimiter= ",") #load params in from the directory
SM_parameters= np.loadtxt("SM_parameters.csv", delimiter= ",")



# In[9]:


SM_parameter_errors


# In[10]:


F_L=[SM_parameters[0][0],     SM_parameters[1][0],     SM_parameters[2][0],     SM_parameters[3][0],     SM_parameters[4][0],     SM_parameters[5][0],     SM_parameters[6][0],     SM_parameters[7][0],     SM_parameters[8][0],     SM_parameters[9][0]]


A_FB=[SM_parameters[0][1],     SM_parameters[1][1],     SM_parameters[2][1],     SM_parameters[3][1],     SM_parameters[4][1],     SM_parameters[5][1],     SM_parameters[6][1],     SM_parameters[7][1],     SM_parameters[8][1],     SM_parameters[9][1]]




S3=[SM_parameters[0][2],     SM_parameters[1][2],     SM_parameters[2][2],     SM_parameters[3][2],     SM_parameters[4][2],     SM_parameters[5][2],     SM_parameters[6][2],     SM_parameters[7][2],     SM_parameters[8][2],     SM_parameters[9][2]]



S4=[SM_parameters[0][3],     SM_parameters[1][3],     SM_parameters[2][3],     SM_parameters[3][3],     SM_parameters[4][3],     SM_parameters[5][3],     SM_parameters[6][3],     SM_parameters[7][3],     SM_parameters[8][3],     SM_parameters[9][3]]


S5=[SM_parameters[0][4],     SM_parameters[1][4],     SM_parameters[2][4],     SM_parameters[3][4],     SM_parameters[4][4],     SM_parameters[5][4],     SM_parameters[6][4],     SM_parameters[7][4],     SM_parameters[8][4],     SM_parameters[9][4]]

S7=[SM_parameters[0][5],     SM_parameters[1][5],     SM_parameters[2][5],     SM_parameters[3][5],     SM_parameters[4][5],     SM_parameters[5][5],     SM_parameters[6][5],     SM_parameters[7][5],     SM_parameters[8][5],     SM_parameters[9][5]]

S8= [SM_parameters[0][6],     SM_parameters[1][6],     SM_parameters[2][6],     SM_parameters[3][6],     SM_parameters[4][6],     SM_parameters[5][6],     SM_parameters[6][6],     SM_parameters[7][6],     SM_parameters[8][6],     SM_parameters[9][6]]

S9=[SM_parameters[0][7],     SM_parameters[1][7],     SM_parameters[2][7],     SM_parameters[3][7],     SM_parameters[4][7],     SM_parameters[5][7],     SM_parameters[6][7],     SM_parameters[7][7],     SM_parameters[8][7],     SM_parameters[9][7]]


# In[11]:


F_L_errors=[SM_parameter_errors[0][0],     SM_parameter_errors[1][0],     SM_parameter_errors[2][0],     SM_parameter_errors[3][0],     SM_parameter_errors[4][0],     SM_parameter_errors[5][0],     SM_parameter_errors[6][0],     SM_parameter_errors[7][0],     SM_parameter_errors[8][0],     SM_parameter_errors[9][0]]


A_FB_errors=[SM_parameter_errors[0][1],     SM_parameter_errors[1][1],     SM_parameter_errors[2][1],     SM_parameter_errors[3][1],     SM_parameter_errors[4][1],     SM_parameter_errors[5][1],     SM_parameter_errors[6][1],     SM_parameter_errors[7][1],     SM_parameter_errors[8][1],     SM_parameter_errors[9][1]]




S3_errors=[SM_parameter_errors[0][2],     SM_parameter_errors[1][2],     SM_parameter_errors[2][2],     SM_parameter_errors[3][2],     SM_parameter_errors[4][2],     SM_parameter_errors[5][2],     SM_parameter_errors[6][2],     SM_parameter_errors[7][2],     SM_parameter_errors[8][2],     SM_parameter_errors[9][2]]



S4_errors=[SM_parameter_errors[0][3],     SM_parameter_errors[1][3],     SM_parameter_errors[2][3],     SM_parameter_errors[3][3],     SM_parameter_errors[4][3],     SM_parameter_errors[5][3],     SM_parameter_errors[6][3],     SM_parameter_errors[7][3],     SM_parameter_errors[8][3],     SM_parameter_errors[9][3]]


S5_errors=[SM_parameter_errors[0][4],     SM_parameter_errors[1][4],     SM_parameter_errors[2][4],     SM_parameter_errors[3][4],     SM_parameter_errors[4][4],     SM_parameter_errors[5][4],     SM_parameter_errors[6][4],     SM_parameter_errors[7][4],     SM_parameter_errors[8][4],     SM_parameter_errors[9][4]]

S7_errors=[SM_parameter_errors[0][5],     SM_parameter_errors[1][5],     SM_parameter_errors[2][5],     SM_parameter_errors[3][5],     SM_parameter_errors[4][5],     SM_parameter_errors[5][5],     SM_parameter_errors[6][5],     SM_parameter_errors[7][5],     SM_parameter_errors[8][5],     SM_parameter_errors[9][5]]

S8_errors= [SM_parameter_errors[0][6],     SM_parameter_errors[1][6],     SM_parameter_errors[2][6],     SM_parameter_errors[3][6],     SM_parameter_errors[4][6],     SM_parameter_errors[5][6],     SM_parameter_errors[6][6],     SM_parameter_errors[7][6],     SM_parameter_errors[8][6],     SM_parameter_errors[9][6]]

S9_errors=[SM_parameter_errors[0][7],     SM_parameter_errors[1][7],     SM_parameter_errors[2][7],     SM_parameter_errors[3][7],     SM_parameter_errors[4][7],     SM_parameter_errors[5][7],     SM_parameter_errors[6][7],     SM_parameter_errors[7][7],     SM_parameter_errors[8][7],     SM_parameter_errors[9][7]]


# In[12]:


bin_0 =[0.1,0.98]
bin_1=[1.1,2.5]
bin_2=[2.5,4.0]
bin_3=[4.0,6.0]
bin_8=[1.1,6.0]
bin_4 =[6.0,8.0]
bin_7 = [11,12.5]
bin_5 = [15,17]
bin_6 = [17,19]
bin_9 =[15,19]


# In[13]:


bin_ranges_defined= [bin_0,bin_1,bin_2,bin_3,bin_4,bin_5,bin_6,bin_7,bin_8,bin_9]
len(bin_ranges_defined)


# In[14]:


SM_predictions=[]

names =['FL','AFB','S3','S4','S5','S7','S8','S9']
for i in names:
    for specific_bin in bin_ranges_defined:
        value=flavio.sm_prediction('<'+ i +'>(B0->K*mumu)',specific_bin[0],specific_bin[1])
        #print(value)
        SM_predictions.append(value)
SM_predictions=np.array(SM_predictions)


# In[15]:


len(SM_predictions)


# In[16]:


F_L


# In[17]:


A_FB


# In[18]:


S3


# In[19]:


S4


# In[20]:


S5


# In[21]:


S7


# In[22]:


S8


# In[23]:


S9


# In[24]:


import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy


def chisqr(obs, exp, error):
    chisqr = 0
    for i in range(len(obs)):
        chisqr = chisqr + ((obs[i] - exp[i]) ** 2) / (error[i] ** 2)
    return chisqr#
def gaussian(x):
    return(1/np.sqrt(2*np.pi)) * np.exp(-0.5*x**2)



sm_observables = np.array([F_L,A_FB,S3,S4,S5,S7,S8,S9])
errors= np.array([F_L_errors,A_FB_errors,S3_errors,S4_errors,S5_errors,S7_errors,S8_errors,S9_errors])
bin_ranges = bin_ranges_defined

# Define a list of numbers
numbers = list(range(80))

# Define an empty list to store the ranges
ranges = []

# Iterate over the ranges of 10
for i in range(0, len(numbers), 10):
    # Append the current range to the list of ranges
    ranges.append(numbers[i:i+10])

# Print the list of ranges
#print(ranges)

for number_val in range(0, len(errors)):
    
    chi_sqr = chisqr(sm_observables[number_val,:],SM_predictions[ranges[number_val]],
                     errors[number_val,:])
    degrees_of_freedom = sm_observables[number_val,:].shape[0] - 1
    reduced_chi_sqr = chi_sqr / degrees_of_freedom
    p = 1 - scipy.stats.chi2.cdf(chi_sqr, degrees_of_freedom)
    print("Reduced Chi Squared for {} = {:.3f}".format(names[number_val],reduced_chi_sqr))
    print("p value = {:.4f}".format(p))

#Calculating p value fitting 

all_vals = sm_observables.flatten()
all_errs = errors.flatten()
chi_sqr = chisqr(all_vals,SM_predictions, all_errs)
degrees_of_freedom = all_vals.shape[0] - 1
reduced_chi_sqr = chi_sqr / degrees_of_freedom
p = 1 - scipy.stats.chi2.cdf(chi_sqr, degrees_of_freedom)
print("Reduced Chi Squared for all observables = {:.3f}".format(reduced_chi_sqr))
print("p value = {:.3f}".format(p))
significance= scipy.integrate.quad(gaussian, 5, np.inf)[0]
if significance>p:
    print("Evidence to suggest SM violation")
else:
    print("No Evidence to suggest SM violation")
    


# In[ ]:
#MH method - 







# In[25]:


len(errors)


# # Analysis of Wilson Coefficients to check for violations

# Define the theoretical function that computes the observable. This can be done using the flavio.physics module. For example, to compute the CP asymmetry in B0 -> K0 pi0, you could use the flavio.physics.decays.bmixing.cp_asymmetry function:
# 
# 
# 

# Add any experimental constraints on the observable using the Observable.add_constraint method.
# For example, if you want to include the experimental measurement of the CP asymmetry in B0 -> K0 pi0 
# from the LHCb collaboration, you could add the following constraint:
# 
# 

# Compute the Standard Model prediction for the observable using the flavio.sm_prediction function:
# 
# 

# Compare the Standard Model prediction to the experimental measurement to see if there is evidence for CP violation. You can use the Observable.get_experimental_result method to retrieve the experimental value and uncertainty:
# 

# $B_0->K^{*}\mu^{+}\mu^{+}$

# In[26]:


import flavio


# In[27]:


bin_0 =[0.1,0.98]
bin_1=[1.1,2.5]
bin_2=[2.5,4.0]
bin_3=[4.0,6.0]
bin_8=[1.1,6.0]
bin_4 =[6.0,8.0]
bin_7 = [11,12.5]
bin_5 = [15,17]
bin_6 = [17,19]
bin_9 =[15,19]


# In[28]:


#bin predictions
flavio.sm_prediction('<S3>(B0->K*mumu)',0.1,0.98)
flavio.sm_uncertainty('<S3>(B0->K*mumu)',0.1,0.98)


# In[29]:


from wilson import Wilson
w = Wilson({ 'CVRR_bdbd': 1e-10, 'CVRR_bsbs': 1e-10 }, scale=160, eft='WET', basis='flavio')


# In[30]:


#CVLR_bbmumu


# In[31]:


flavio.np_prediction('<A3>(B0->K*mumu)', w,0.1,0.98)


# In[32]:


par_dict = flavio.default_parameters.get_central_all()
par_dict
par_diction =par_dict


# In[33]:


flavio.parameters


# In[34]:


r"""$\Delta F=2$ Wilson coefficient in the Standard Model."""

from math import log,pi,sqrt
from flavio.physics.mesonmixing.common import meson_quark
from flavio.physics import ckm
import flavio

def F_box(x, y):
    r"""$\Delta F=2$ box loop function.
    Parameters
    ----------
    - `x`:
        $m_{u_i}^2/m_W^2$
    - `y`:
        $m_{u_j}^2/m_W^2$
    """
    if x == y:
        return ((4+4 * x-15 * x**2+x**3)/(4 * (-1+x)**2)
              +(x * (-4+4 * x+3 * x**2) * log(x))/(2 * (-1+x)**3))
    return ((4-7 * x * y)/(4-4 * x-4 * y+4 * x * y)
        +(x**2 * (4+(-8+x) * y) * log(x))/(4 * (-1+x)**2 * (x-y))
        -((4+x * (-8+y)) * y**2 * log(y))/(4 * (x-y) * (-1+y)**2))

def S0_box(x, y, xu=0):
    r"""$\Delta F=2$ box loop function $S_0(x, y, x_u)$."""
    flavio.citations.register("Inami:1980fz")
    return F_box(x, y) + F_box(xu, xu) - F_box(x, xu) - F_box(y, xu)

def df2_prefactor(par):
    GF = par['GF']
    mW = par['m_W']
    return -GF**2/(4.*pi**2) * mW**2


def cvll_d(par, meson, scale=160):
    r"""Contributions to the Standard Model Wilson coefficient $C_V^{LL}$
    for $B^0$, $B_s$, and $K$ mixing at the matching scale.
    The Hamiltonian is defined as
    $$\mathcal H_{\mathrm{eff}} = - C_V^{LL} O_V^{LL},$$
    where $O_V^{LL} = (\bar d_L^i\gamma^\mu d_L^j)^2$ with $i<j$.
    Parameters
    ----------
    - `par`:
        parameter dictionary
    - `meson`:
        should be one of: 'B0' or 'K0'
    Returns
    -------
    a tuple of three complex numbers `(C_tt, C_cc, C_ct)` that contain the top-,
    charm-, and charm-top-contribution to the Wilson coefficient. This
    separation is necessary as they run differently.
    """
    mt = flavio.physics.running.running.get_mt_mt(par)
    mc = par["m_c"]
    mu = par["m_u"]
    mW = par['m_W']
    xt = mt**2/mW**2
    xc = mc**2/mW**2
    xu = mu**2/mW**2
    di_dj = meson_quark[meson]
    xi_t = ckm.xi('t',di_dj)(par)
    xi_c = ckm.xi('c',di_dj)(par)
    N = df2_prefactor(par)
    C_cc = N * xi_c**2     * S0_box(xc, xc, xu)
    C_tt = N * xi_t**2     * S0_box(xt, xt, xu)
    C_ct = N * 2*xi_c*xi_t * S0_box(xc, xt, xu)
    return (C_tt, C_cc, C_ct)


# In[35]:


cvll_d(par_dict,'B0')


# In[36]:


def wc_btos(par_dict, scale, nf_out=5):
    alpha_s = flavio.physics.running.running.get_alpha_s(par, scale)
    wc = cvll_d(par_dict,'B0')
    return wc['C9_bsmumu'], wc['C10_bsmumu']


def wc_fct(C9pRe, C9pIm):
    return { 'C9p_bs': C9pRe + 1j * C9pIm, }

# This function returns a tuple (C9, C10) of complex numbers containing the values 
# of the Wilson coefficients at the given scale scale. The par argument is a 
# dictionary of SM parameters, and nf_out specifies
# the number of active quark flavors in the effective theory 
# below the matching scale (usually taken to be the charm mass)

# In[37]:





par_diction = flavio.default_parameters.get_central_all()
wc_obj = flavio.WilsonCoefficients()


# In[38]:


#wc_obj


# In[ ]:





# In[39]:


names =['FL','AFB','S3','S4','S5','S7','S8','S9']
observables = []
for i in names:
    for specific_bin in bin_ranges_defined:
        my_observable= ('<'+i+'>(B0->K*mumu)',specific_bin[0],specific_bin[1]) 
        #print(my_observable)
        observables.append(my_observable)


# In[40]:


#observables= [('<AFB>(B0->K*mumu)', 11, 12.5)]


# In[41]:


bin_0 =[0.1,0.98]
bin_1=[1.1,2.5]
bin_2=[2.5,4.0]
bin_3=[4.0,6.0]
bin_8=[1.1,6.0]
bin_4 =[6.0,8.0]
bin_7 = [11,12.5]
bin_5 = [15,17]
bin_6 = [17,19]
bin_9 =[15,19]


# In[42]:


def fastfit_obs(name, obslist):
    return flavio.statistics.likelihood.FastLikelihood(
                name = name,
                observables = obslist,
                fit_parameters = wc_fct)


# In[43]:


#C9
fits = OrderedDict()
minim,maxim=1,9
for num,i in enumerate(names):
    fits[i] =observables[minim:maxim]
    minim +=10
    maxim +=10
"""
fits = OrderedDict()
##test
fits['AFB']=  observables  
"""




obs_fastfits={}
for k, v in fits.items():
    print(v)
    obs_fastfits[k] = fastfit_obs('C9-C9p fit '+ k, v)

  
global_fastfit = fastfit_obs('C9-C9p fit global', observables)

#labels = {'S3':flavio.Observable.get_instance(fits['S3'][0][0]).tex}


# In[44]:


global_fastfit = fastfit_obs('C9-C9p fit global', observables)


# In[45]:


fits.items


# In[46]:


#[ranges[num]]



# In[47]:


fits


# In[ ]:





# In[ ]:



for k, v in fits.items():
    obs_fastfits[k].make_measurement(threads=1)
global_fastfit.make_measurement(threads=1)


# In[ ]:

loglikelihood_array=[]
for i, f in enumerate(fits):
    g= obs_fastfits[f].log_likelihood(par_diction, wc_obj)
    print(f,g)
    loglikelihood_array.append([f,g])
print(loglikelihood_array)    
result =global_fastfit.log_likelihood(par_diction, wc_obj)
print('total:',result)

# In[ ]:


#global_fastfit.log_likelihood(par_diction, wc_obj)


# In[ ]:


#contour plot # below


# In[ ]:


def globalfitfuncredefined():
    glob_val=global_fastfit.log_likelihood(par_diction, wc_obj)
    return global_fastfit.log_likelihood

def fastfitfuncredefined(f):
    fast_val=obs_fastfits[f].log_likelihood(par_diction, wc_obj)
    return fast_val


# In[ ]:
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)


fig=plt.figure(figsize=(4,4))
x_max=0.33
plt.xlim([-0.3,0.3])
plt.ylim([-0.3,0.3])

#add labels label=labels[f]
for i, f in enumerate(fits):
    flavio.plots.plotfunctions.likelihood_contour(fastfitfuncredefined(f),
                                    -x_max, x_max, -x_max, x_max, col=i+1,
                                    interpolation_factor=3, threads=1, steps=1)

flavio.plots.plotfunctions.likelihood_contour(globalfitfuncredefined,
                                -x_max, x_max, -x_max, x_max, n_sigma=(1, 2), col=0,
                                interpolation_factor=4, threads=1, steps=1, label='global')

# labels, legend
#plt.xlabel(r'$\text{Re}(C_9^{\prime\,\text{NP}})$')
#plt.ylabel(r'$\text{Re}(C_10^\prime)$')
plt.legend(loc=2, bbox_to_anchor=(1.05, 1))


# In[ ]:


fig=plt.figure(figsize=(4,4))
x_max=0.33
plt.xlim([-0.3,0.3])
plt.ylim([-0.3,0.3])

#add labels label=labels[f]
for i, f in enumerate(fits):
    flavio.plots.plotfunctions.likelihood_contour(fastfitfuncredefined,
                                    -x_max, x_max, -x_max, x_max, col=i+1,
                                    interpolation_factor=3, threads=1, steps=1)

flavio.plots.plotfunctions.likelihood_contour(globalfitfuncredefined(par_diction,wc_obj),
                                -x_max, x_max, -x_max, x_max, n_sigma=(1, 2), col=0,
                                interpolation_factor=10, threads=1, steps=1, label='global')

# labels, legend
plt.xlabel(r'$\text{Re}(C_9^{\prime\,\text{NP}})$')
plt.ylabel(r'$\text{Re}(C_10^\prime)$')
plt.legend(loc=2, bbox_to_anchor=(1.05, 1))


# In[ ]:


#dir(obs_fastfits['ATIm'])



# In[ ]:


# In[ ]:




