# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 15:54:35 2023

@author: Utilisateur
"""

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
#%% load tthe sig data file to test 
data_sig=pd.read_csv('../data/sig.csv',delimiter=',')
#%%
c=3e8
particles=['mu_plus','mu_minus','K','Pi']
masses=[105.658,105.658,493.677,139.570] #MeV/c^2

#%%
def Cherenkov_angle(p,mass):
    p_2=p*p
    if p<40000:
        n=1.0014
    else:
        n=1.0005
    cos_theta_c=np.sqrt(mass*mass+p_2)/(p*n)
    if cos_theta_c>1:
        theta_c=1000 #value of 1000 indicates that the momentum is too small
    else:
        theta_c=np.arccos(cos_theta_c)
    return theta_c

#%%
theta_c_sig=np.zeros((len(data_sig['mu_plus_P']),4))

for i in range(0,4):
    p=np.array(data_sig[f'{particles[i]}_P'])
    for j in range (0,len(data_sig['mu_plus_P'])):
        theta_c_sig[j,i]=Cherenkov_angle(p[j],masses[i])
    

#%%
K_small=np.where(theta_c_sig[:,2]>500)[0]
Pi_small=np.where(theta_c_sig[:,3]>500)[0]

theta_c_K=np.delete(theta_c_sig[:,2],K_small)
theta_c_Pi=np.delete(theta_c_sig[:,3],Pi_small)
theta_c_mu_p=theta_c_sig[:,0]
theta_c_mu_m=theta_c_sig[:,1]
K_P=data_sig['K_P'].drop(index=K_small)/1e3
Pi_P=data_sig['Pi_P'].drop(index=Pi_small)/1e3

#%%
plt.figure(1)
plt.plot(data_sig['mu_plus_P']/1e3,theta_c_mu_p,'x',label=r'$\mu^{+}$')
plt.plot(data_sig['mu_minus_P']/1e3,theta_c_mu_m,'x',label=r'$\mu^{-}$')
plt.plot(K_P,theta_c_K,'x',label='K')
plt.plot(Pi_P,theta_c_Pi,'x',label=r'$\pi$')
plt.xscale('log')
plt.title('Cherenkov angle vs momentum for the signal decay')
plt.xlabel('momentum (GeV)')
plt.ylabel(r'$\theta_c$')
plt.legend()
plt.show()

#%%
mu_m_hist=plt.hist(theta_c_mu_m,bins=200,density=True)
mu_p_hist=plt.hist(theta_c_mu_p,bins=200,density=True)
K_hist=plt.hist(theta_c_K,bins=200,density=True)
Pi_hist=plt.hist(theta_c_Pi,bins=200,density=True)



#%%
from scipy.optimize import curve_fit

def Exp_dist(x,lamb,c,a):
    f_x=lamb*np.exp(a*(x+c))
    return f_x
x_coords=np.zeros(len(mu_m_hist[0]))
for i in range(0,len(mu_m_hist[0])):
    x_coords[i]=(mu_m_hist[1][i]+mu_m_hist[1][i+1])/2

initial_guess=[1,-0.05,2000]

fit_mu_m=curve_fit(Exp_dist,x_coords,mu_m_hist[0],initial_guess)
print(fit_mu_m)
fit_data=Exp_dist(np.linspace(0.040,0.053,500),*fit_mu_m[0])


plt.hist(theta_c_mu_m,bins=500,density=True)
plt.plot(np.linspace(0.040,0.053,500), fit_data)
plt.show()





