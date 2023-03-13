#!/usr/bin/env python
"""
Created on Sun March 12 2023
@author: Regen Petu-Stiles
"""
# coding: utf-8

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


# Define the observable you want to study using the Flavio Observable class. For example, if you want to study the CP asymmetry in the decay B0 -> K0 pi0, you could define the observable as follows:
# 
# 

# To calculate the Wilson coefficients from angular observables in bins of q2, you can use the wilsoncoefficients.wilson_coefficients function. Example below

# In[20]:


import flavio.physics.mesonmixing.wilsoncoefficient as wilson_coefficients


# In[29]:


flavio.physics.mesonmixing.observables.Observable('ACP(B0->K0pi0)')


# In[34]:


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

s = 1.519267515435317e+24

c = copy.deepcopy(default_parameters)
par = c.get_central_all()

wc_obj = WilsonCoefficients()
wc_B0 = wc_obj.get_wc('bdbd', 4.2, par)
CVSM = flavio.physics.mesonmixing.wilsoncoefficient.cvll_d(par, 'B0', scale=80)[0]
w = Wilson({'CVRR_bdbd': CVSM}, 80, 'WET', 'flavio')
flavio.np_prediction('DeltaM_d', w) / flavio.sm_prediction('DeltaM_d')


# In[37]:





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

# In[18]:


import flavio


# In[154]:


#bin predictions
flavio.sm_prediction('<A3>(B0->K*mumu)',0.1,0.98)
flavio.sm_uncertainty('<A3>(B0->K*mumu)',0.1,0.98)


# In[27]:


from wilson import Wilson
w = Wilson({ 'CVRR_bdbd': 1e-10, 'CVRR_bsbs': 1e-10 }, scale=160, eft='WET', basis='flavio')


# In[ ]:


#CVLR_bbmumu


# In[30]:


flavio.np_prediction('<A3>(B0->K*mumu)', w,0.1,0.98)


# In[66]:


par_dict = flavio.default_parameters.get_central_all()
par_dict
par_diction =par_dict


# In[65]:


flavio.parameters


# In[49]:


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


# In[69]:


cvll_d(par_dict,'B0')


# In[39]:


dir(flavio.statistics.likelihood)


# In[ ]:


'B0->K*0 deltaC9 c_0 Re': 0.0,
 'B+->K*+ deltaC9 c_0 Re': 0.0,
 'Bs->phi deltaC9 c_0 Re': 0.0,
 'B0->K*0 deltaC9 c_0 Im': 0.0,
 'B+->K*+ deltaC9 c_0 Im': 0.0,
 'Bs->phi deltaC9 c_0 Im': 0.0,
 'B0->K*0 deltaC9 c_+ Re': 0.0,
 'B+->K*+ deltaC9 c_+ Re': 0.0,
 'Bs->phi deltaC9 c_+ Re': 0.0,
 'B0->K*0 deltaC9 c_+ Im': 0.0,
 'B+->K*+ deltaC9 c_+ Im': 0.0,
 'Bs->phi deltaC9 c_+ Im': 0.0,
 'B0->K*0 deltaC9 c_- Re': 0.0,
 'B+->K*+ deltaC9 c_- Re': 0.0,
 'Bs->phi deltaC9 c_- Re': 0.0,
 'B0->K*0 deltaC9 c_- Im': 0.0,
 'B+->K*+ deltaC9 c_- Im': 0.0,
 'Bs->phi deltaC9 c_- Im': 0.0,
 'B0->K0 deltaC9 a Re': 0.0,
 'B+->K+ deltaC9 a Re': 0.0,
 'B0->K0 deltaC9 a Im': 0.0,
 'B+->K+ deltaC9 a Im': 0.0,
 'B0->K0 deltaC9 b Re': 0.0,
 'B+->K+ deltaC9 b Re': 0.0,
 'B0->K0 deltaC9 b Im': 0.0,
 'B+->K+ deltaC9 b Im': 0.0,
 'B0->K0 deltaC9 c Re': 0.0,
 'B+->K+ deltaC9 c Re': 0.0,
 'B0->K0 deltaC9 c Im': 0.0,
 'B+->K+ deltaC9 c Im': 0.0,


# In[78]:


def wc_btos(par_dict, scale, nf_out=5):
    alpha_s = flavio.physics.running.running.get_alpha_s(par, scale)
    wc = cvll_d(par_dict,'B0')
    return wc['C9_bsmumu'], wc['C10_bsmumu']




# This function returns a tuple (C9, C10) of complex numbers containing the values 
# of the Wilson coefficients at the given scale scale. The par argument is a 
# dictionary of SM parameters, and nf_out specifies
# the number of active quark flavors in the effective theory 
# below the matching scale (usually taken to be the charm mass)

# In[119]:


import unittest
import flavio
from flavio.physics.taudecays import taulnunu
from wilson import Wilson
from math import sqrt


par_diction = flavio.default_parameters.get_central_all()
wc_obj = flavio.WilsonCoefficients()


# In[120]:


import flavio
import flavio.plots
import flavio.statistics.likelihood
import matplotlib.pyplot as plt
from collections import OrderedDict


# In[172]:


observables = [
  'BR(B+->K*gamma)',
  'BR(B->Xsgamma)',
  'BR(B0->K*gamma)',
  'BR(Bs->phigamma)',
  'ADeltaGamma(Bs->phigamma)',
  'S_K*gamma',
  ('<ATIm>(B0->K*ee)', 0.002, 1.12),
  ('<P1>(B0->K*ee)', 0.002, 1.12),
   ('<A3>(B0->K*mumu)',0.1,0.98) 
]


# In[ ]:





# In[173]:


def fastfit_obs(name, obslist):
    return flavio.statistics.likelihood.FastLikelihood(
                name = name,
                observables = obslist)


# In[174]:


fits = OrderedDict()
fits['BR'] = ['BR(B+->K*gamma)', 'BR(B->Xsgamma)', 'BR(B0->K*gamma)', 'BR(Bs->phigamma)',]
fits['A'] = ['ADeltaGamma(Bs->phigamma)']
fits['P1'] = [('<P1>(B0->K*ee)', 0.002, 1.12)]
fits['S'] = ['S_K*gamma']
fits['ATIm'] = [('<ATIm>(B0->K*ee)', 0.002, 1.12)]
fits['<A3>']=[('<A3>(B0->K*mumu)',0.1,0.98)]

obs_fastfits={}
for k, v in fits.items():
    obs_fastfits[k] = fastfit_obs('C9-C9p fit '+ k, v)

global_fastfit = fastfit_obs('C9-C9p fit global', observables)


# In[175]:


labels = {
    'BR': 'branching ratios',
    'A': flavio.Observable.get_instance(fits['A'][0]).tex,
    'S': flavio.Observable.get_instance(fits['S'][0]).tex,
    'ATIm': flavio.Observable.get_instance(fits['ATIm'][0][0]).tex,
    'P1': flavio.Observable.get_instance(fits['P1'][0][0]).tex,
    '<A3>':flavio.Observable.get_instance(fits['<A3>'][0][0]).tex
    
}


# In[177]:


get_ipython().run_cell_magic('time', '', 'for k, v in fits.items():\n    obs_fastfits[k].make_measurement(threads=4)\nglobal_fastfit.make_measurement(threads=4)')


# In[178]:


for i, f in enumerate(fits):
    g= obs_fastfits[f].log_likelihood(par_diction, wc_obj)
    print(f,g)


# In[ ]:


#Trying  to get a contour plot # below - WIP


# In[149]:


from flavio.statistics.functions import delta_chi2, confidence_level

def likelihood_contour_data(mylog_likelihood, x_min, x_max, y_min, y_max,
              n_sigma=1, steps=20, threads=1, pool=None):
    r"""Generate data required to plot coloured confidence contours (or bands)
    given a log likelihood function.
    Parameters:
    - `log_likelihood`: function returning the logarithm of the likelihood.
      Can e.g. be the method of the same name of a FastFit instance.
    - `x_min`, `x_max`, `y_min`, `y_max`: data boundaries
    - `n_sigma`: plot confidence level corresponding to this number of standard
      deviations. Either a number (defaults to 1) or a tuple to plot several
      contours.
    - `steps`: number of grid steps in each dimension (total computing time is
      this number squared times the computing time of one `log_likelihood` call!)
    - `threads`: number of threads, defaults to 1. If greater than one,
      computation of z values will be done in parallel.
    - `pool`: an instance of `multiprocessing.Pool` (or a compatible
    implementation, e.g. from `multiprocess` or `schwimmbad`). Overrides the
    `threads` argument.
    """
    _x = np.linspace(x_min, x_max, steps)
    _y = np.linspace(y_min, y_max, steps)
    x, y = np.meshgrid(_x, _y)
    if threads == 1:
        @np.vectorize
        def chi2_vect(x, y): # needed for evaluation on meshgrid
            return -2*mylog_likelihood([x,y])
        z = chi2_vect(x, y)
    else:
        xy = np.array([x, y]).reshape(2, steps**2).T
        try:
            z = -2*np.array(pool.map(mylog_likelihood, xy )).reshape((steps, steps))
        except PicklingError:
            raise PicklingError("When using more than 1 thread, the "
                                "log_likelihood function must be picklable; "
                                "in particular, you cannot use lambda expressions.")

    # get the correct values for 2D confidence/credibility contours for n sigma
    if isinstance(n_sigma, Number):
        levels = [delta_chi2(n_sigma, dof=2)]
    else:
        levels = [delta_chi2(n, dof=2) for n in n_sigma]
    return {'x': x, 'y': y, 'z': z, 'levels': levels}


def likelihood_contour(mylog_likelihood, x_min, x_max, y_min, y_max,
              n_sigma=1, steps=20, threads=1,
              **kwargs):
    r"""Plot coloured confidence contours (or bands) given a log likelihood
    function.
    Parameters:
    - `log_likelihood`: function returning the logarithm of the likelihood.
      Can e.g. be the method of the same name of a FastFit instance.
    - `x_min`, `x_max`, `y_min`, `y_max`: data boundaries
    - `n_sigma`: plot confidence level corresponding to this number of standard
      deviations. Either a number (defaults to 1) or a tuple to plot several
      contours.
    - `steps`: number of grid steps in each dimension (total computing time is
      this number squared times the computing time of one `log_likelihood` call!)
    All remaining keyword arguments are passed to the `contour` function
    and allow to control the presentation of the plot (see docstring of
    `flavio.plots.plotfunctions.contour`).
    """
    data = likelihood_contour_data(mylog_likelihood=mylog_likelihood,
                                x_min=x_min, x_max=x_max,
                                y_min=y_min, y_max=y_max,
                                n_sigma=n_sigma, steps=steps, threads=threads)
    data.update(**kwargs) #  since we cannot do **data, **kwargs in Python <3.5
    return contour(**data)


# In[180]:


get_ipython().run_cell_magic('time', '', "fig=plt.figure(figsize=(4,4))\nx_max=0.33\nplt.xlim([-0.3,0.3])\nplt.ylim([-0.3,0.3])\n\n#add labels label=labels[f]\nfor i, f in enumerate(fits):\n    flavio.plots.plotfunctions.likelihood_contour(obs_fastfits[f].log_likelihood(par_diction, wc_obj),\n                                    -x_max, x_max, -x_max, x_max, col=i+1,\n                                    interpolation_factor=3, threads=4, steps=30)\n\nflavio.plots.plotfunctions.likelihood_contour(global_fastfit.log_likelihood(par_diction, wc_obj),\n                                -x_max, x_max, -x_max, x_max, n_sigma=(1, 2), col=0,\n                                interpolation_factor=10, threads=4, steps=30, label='global')\n\n# labels, legend\nplt.xlabel(r'$\\text{Re}(C_7^{\\prime\\,\\text{NP}})$')\nplt.ylabel(r'$\\text{Im}(C_7^\\prime)$')\nplt.legend(loc=2, bbox_to_anchor=(1.05, 1))")


# In[162]:





# In[159]:


f


# In[ ]:




