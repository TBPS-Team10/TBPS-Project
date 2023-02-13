# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 00:40:48 2023

@author: Louis Beucher
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import Selection_criteria_func #need the filtering file in the same directory
from scipy.optimize import curve_fit
import Outlier_removal
#%% this cell filters the data using Aisulu filter only
# add any additional file names you wish to use. Not using jpsi and psi2S as assuming they are already fully filtered out
filenames = ["Jpsi_Kstarp_pi0.csv", "jpsi_mu_k_swap.csv",
             "jpsi_mu_pi_swap.csv", "k_pi_swap.csv", "Kmumu.csv", "Kstarp_pi0.csv",
             "phimumu.csv", "pKmumu_piTok_kTop.csv", "pKmumu_piTop.csv"]
#keeping correct order is important

#%% using aisulu's filter, only choose one of the filtering cells
for name in filenames:
    data = pd.read_csv(f"data/{name}", delimiter=",") #load datafile, add ./data if required 
    print('initial length',len(data))
    Selection_criteria_func.select(data) #select data using filtering method, filtering method may be changed
    print('length after A filter',len(data))
    if name=="Jpsi_Kstarp_pi0.csv":
        tot_filtered_data=data
    else:
        tot_filtered_data=pd.concat([tot_filtered_data,data],ignore_index=True)

print('the length of the combined filtered simulated datasets is:',len(tot_filtered_data))
    
#%% using avi's outlier filter

for name in filenames:
    data=Outlier_removal.filter_events('data/sig.csv',f"data/{name}")
    print('length after A filter',len(data))
    if name=="Jpsi_Kstarp_pi0.csv":
        tot_filtered_data=data
    else:
        tot_filtered_data=pd.concat([tot_filtered_data,data],ignore_index=True)

print('the length of the combined filtered simulated datasets is:',len(tot_filtered_data))

   


#%% this file uses the post filter ML model in addition 
#not doing it just yet as already losing quite a large amount of data due to severityof filtering

#%% plotting relevant distributions for all bins mixed
sig=pd.read_csv('data/sig.csv',delimiter=',')

plt.subplot(2,2,1)
plt.hist(sig['q2'],alpha=0.8,color='blue',label='signal data',bins=50,density=True)
plt.hist(tot_filtered_data['q2'],alpha=0.5,color='red',label='simulated filtered data',bins=50,density=True)
plt.legend()
plt.xlabel(r'$q^2$')
plt.ylabel('frequency')
plt.title('q2 for signal and filtered simulated data')

plt.subplot(2,2,2)
plt.hist(sig['costhetal'],alpha=0.8,color='blue',label='signal data',bins=50,density=True)
plt.hist(tot_filtered_data['costhetal'],alpha=0.5,color='red',label='simulated filtered data',bins=50,density=True)
plt.legend()
plt.xlabel(r'$cos\theta_L$')
plt.ylabel('frequency')
plt.title(r'$cos\theta_L$ for signal and filtered simulated data')

plt.subplot(2,2,3)
plt.hist(sig['costhetak'],alpha=0.8,color='blue',label='signal data',bins=50,density=True)
plt.hist(tot_filtered_data['costhetak'],alpha=0.5,color='red',label='simulated filtered data',bins=50,density=True)
plt.legend()
plt.xlabel(r'$cos\theta_k$')
plt.ylabel('frequency')
plt.title(r'$cos\theta_k$ for signal and filtered simulated data')

plt.subplot(2,2,4)
plt.hist(sig['phi'],alpha=0.8,color='blue',label='signal data',bins=50,density=True)
plt.hist(tot_filtered_data['phi'],alpha=0.5,color='red',label='simulated filtered data',bins=50,density=True)
plt.legend()
plt.xlabel(r'$\Phi$')
plt.ylabel('frequency')
plt.title(r'$\Phi$ for signal and filtered simulated data')

#%% separating into bins of q2
#using the bins provided by Mitesh
def bin_separation(df):
    bin_0=df.loc[(df['q2']>=0.1) & (df['q2']<=0.98)]
    bin_1=df.loc[(df['q2']>=1.1) & (df['q2']<=2.5)]
    bin_2=df.loc[(df['q2']>2.5) & (df['q2']<=4.0)]
    bin_3=df.loc[(df['q2']>4.0) & (df['q2']<=6.0)]
    bin_4=df.loc[(df['q2']>6.0) & (df['q2']<=8.0)]
    bin_5=df.loc[(df['q2']>=15.0) & (df['q2']<=17.0)]
    bin_6=df.loc[(df['q2']>17.0) & (df['q2']<=19.0)]
    bin_7=df.loc[(df['q2']>=11.0) & (df['q2']<=12.5)]
    bin_8=df.loc[(df['q2']>=1.0) & (df['q2']<=6.0)]
    bin_9=df.loc[(df['q2']>=15.0) & (df['q2']<=19.0)]
    return bin_0,bin_1,bin_2,bin_3,bin_4,bin_5,bin_6,bin_7,bin_8,bin_9


#%% create the different bins and plot the relevant ones
all_bins=bin_separation(tot_filtered_data)
bin_num=0
all_sig_bins=bin_separation(sig)
bin_q=all_bins[bin_num]
bin_sig=all_sig_bins[bin_num]

plt.subplot(2,2,1)
plt.hist(bin_sig['q2'],alpha=0.8,color='blue',label='signal data',bins=20,density=True)
plt.hist(bin_q['q2'],alpha=0.5,color='red',label='simulated filtered data',bins=20,density=True)
plt.legend()
plt.xlabel(r'$q^2$')
plt.ylabel('frequency')
plt.title(fr'filtered bin {bin_num} $q^2$ against sig')

plt.subplot(2,2,2)
plt.hist(bin_sig['costhetal'],alpha=0.8,color='blue',label='signal data',bins=20,density=True)
plt.hist(bin_q['costhetal'],alpha=0.5,color='red',label='simulated filtered data',bins=20,density=True)
plt.legend()
plt.xlabel(r'$cos\theta_L$')
plt.ylabel('frequency')
plt.title(fr'filtered bin {bin_num} $cos\theta_L$ against sig')

plt.subplot(2,2,3)
plt.hist(bin_sig['costhetak'],alpha=0.8,color='blue',label='signal data',bins=20,density=True)
plt.hist(bin_q['costhetak'],alpha=0.5,color='red',label='simulated filtered data',bins=20,density=True)
plt.legend()
plt.xlabel(r'$cos\theta_k$')
plt.ylabel('frequency')
plt.title(fr'filtered bin {bin_num} $cos\theta_k$ against sig')

plt.subplot(2,2,4)
plt.hist(bin_sig['phi'],alpha=0.8,color='blue',label='signal data',bins=20,density=True)
plt.hist(bin_q['phi'],alpha=0.5,color='red',label='simulated filtered data',bins=20,density=True)
plt.legend()
plt.xlabel(r'$\Phi$')
plt.ylabel('frequency')
plt.title(fr'filtered bin {bin_num} $\Phi$ against sig')

plt.suptitle(fr'angular and $q^2$ distriubtions for bin {bin_num}')

#%% fitting for bins of q2 attempting fit with Chebychev polynomial of the first kind

#create the values taken by the Chebychev polynomials

def Chebyshev_polynomial(x,order): #maximum order is 7
    T=np.zeros((order+1,len(x)))
    

    T[0,:]=np.ones((1,len(x)))
    if order>0:
        T[1,:]=x
        if order>1:
            for i in range(2,order+1):
                T[i,:]=2*np.multiply(x,T[i-1,:])-T[i-2,:]
    
    return T


def fit_Chebyshev_2(x,a,b,c):
    '''
    Parameters
    ----------
    a,b,c :coefficients of the fit
    x : angular data to be fitted
    max_order : order of the Chebychev polynomial

    Returns
    -------
    fit_polynomial: sum of different orders Chebychev polynomials with max_order+1 terms

    '''
    func=Chebyshev_polynomial(x,2)
    fit_polynomial=a*func[0,:]+b*func[1,:]+c*func[2,:]
    
    return fit_polynomial

def fit_Chebyshev_3(x,a,b,c,d):

    func=Chebyshev_polynomial(x,3)
    fit_polynomial=a*func[0,:]+b*func[1,:]+c*func[2,:]+d*func[3,:]
    
    return fit_polynomial
    
def fit_Chebyshev_4(x,a,b,c,d,e):

    func=Chebyshev_polynomial(x,4)
    fit_polynomial=a*func[0,:]+b*func[1,:]+c*func[2,:]+d*func[3,:]+e*func[4,:]
    
    return fit_polynomial

def fit_Chebyshev_5(x,a,b,c,d,e,f):

    func=Chebyshev_polynomial(x,5)
    fit_polynomial=a*func[0,:]+b*func[1,:]+c*func[2,:]+d*func[3,:]+e*func[4,:]+f*func[5,:]
    
    return fit_polynomial
    
def fit_Chebyshev_6(x,a,b,c,d,e,f,g):

    func=Chebyshev_polynomial(x,6)
    fit_polynomial=a*func[0,:]+b*func[1,:]+c*func[2,:]+d*func[3,:]+e*func[4,:]+f*func[5,:]+g*func[6,:]
    
    return fit_polynomial

def fit_Chebyshev_7(x,a,b,c,d,e,f,g,h):

    func=Chebyshev_polynomial(x,7)
    fit_polynomial=a*func[0,:]+b*func[1,:]+c*func[2,:]+d*func[3,:]+e*func[4,:]+f*func[5,:]+g*func[6,:]+h*func[7,:]
    
    return fit_polynomial

def normalise_phi(phi):
    # want phi to be comprised between 1 and -1
    phi_norm=phi/(np.pi)
    return phi_norm
    
def bin_mid(bin_edges):
    #return the coordinate of the middle of the bin rather than its edges
    bin_mid=[]
    for i in range(0,len(bin_edges)-1):
        bin_mid.append((bin_edges[i]+bin_edges[i+1])/2)
    
    return bin_mid
    

def select_Chebyshev_fit(max_order):
    if max_order==2:
        fit_Chebyshev=fit_Chebyshev_2
    if max_order==3:
        fit_Chebyshev=fit_Chebyshev_3
    if max_order==4:
        fit_Chebyshev=fit_Chebyshev_4
    if max_order==5:
        fit_Chebyshev=fit_Chebyshev_5
    if max_order==6:
        fit_Chebyshev=fit_Chebyshev_6
    if max_order==7:
        fit_Chebyshev=fit_Chebyshev_7
    return fit_Chebyshev

def fit_exponential(x,a,b,c):
    return a*np.exp(b*(x-c))    


def find_residuals(y_dat,fit_dat):
    num_dat=len(y_dat)
    res=y_dat-fit_dat
    res2=res**2
    return np.sum(res2)/num_dat

def plot_fit(angle_data,fit_dat,bins,angular_variable=r'cos$\theta_k$'):
    freq,bin_edges,_=plt.hist(angle_data,bins=bins,density=True)
    x_dat=bin_mid(bin_edges)
    plt.plot(x_dat,freq,'x',label='simulated data')
    plt.plot(x_dat,fit_dat,label='fit data')
    plt.xlabel(angular_variable)
    plt.ylabel('frequency')
    plt.legend()
    
    
def make_fit_Chebyshev(angle_data,max_order):
    freq,bin_edges=np.histogram(angle_data,bins=20,density=True)
    x_dat=bin_mid(bin_edges)
    #starting with a flat initial guess and praying for the best
    initial_guess=0.2*np.ones(max_order+1)
    fit_Chebyshev=select_Chebyshev_fit(max_order)
    fit_params,cov_params=curve_fit(fit_Chebyshev,x_dat,freq,p0=initial_guess)
    fit_dat=fit_Chebyshev(x_dat,*fit_params)
    res_val=find_residuals(freq,fit_dat)
    
    return fit_params, cov_params, fit_dat, res_val

def make_fit_exponential(angle_data):
    freq,bin_edges=np.histogram(angle_data,bins=20,density=True)
    x_dat=bin_mid(bin_edges)
    #starting with a flat initial guess and praying for the best
    initial_guess=0.2*np.ones(3)
    fit_params,cov_params=curve_fit(fit_exponential,x_dat,freq,p0=initial_guess)
    fit_dat=fit_exponential(x_dat,*fit_params)
    res_val=find_residuals(freq,fit_dat)
    
    return fit_params, cov_params, fit_dat, res_val

def find_best_fit(angle_data,max_order):
    best_fit_params=0
    best_cov_params=0
    best_fit_dat=0
    best_res_val=1e20
    best_order=0
    for i in range(2,max_order+1):
    
        fit_params,cov_params,fit_dat,res_val=make_fit_Chebyshev(angle_data,i)
        if res_val<best_res_val:
            best_fit_params=fit_params
            best_cov_params=cov_params
            best_fit_dat=fit_dat
            best_res_val=res_val
            best_order=i
    
    fit_params_exp, cov_params_exp, fit_dat_exp, res_val_exp=make_fit_exponential(angle_data)
    if res_val_exp<res_val:
        best_fit_params=fit_params_exp
        best_cov_params=cov_params_exp
        best_fit_dat=fit_dat_exp
        best_res_val=res_val_exp
        best_order=1000 #the exponential is the best will be called 1000
    
    
    
    return best_fit_params, best_cov_params, fit_dat, best_res_val, best_order



def make_all_fits(bin_dat,q2bin_num,max_order):
    cosl_vals=find_best_fit(np.array(bin_dat['costhetal']),max_order)
    cosk_vals=find_best_fit(np.array(bin_dat['costhetak']),max_order)
    phi_vals=find_best_fit(np.array(bin_dat['phi']),max_order)
    
    plt.figure(q2bin_num)
    plt.subplot(1,3,1)
    plot_fit(bin_dat['costhetal'],cosl_vals[2],20,angular_variable=r'cos$\theta_l$')
    plt.subplot(1,3,2)
    plot_fit(bin_dat['costhetak'],cosk_vals[2],20,angular_variable=r'cos$\theta_k$)')
    plt.subplot(1,3,3)
    plot_fit(bin_dat['phi'],phi_vals[2],20,angular_variable=r'$\Phi$')
    plt.suptitle(f'background fit for bin {q2bin_num}',fontweight='bold')
    plt.show()
    
    return cosl_vals, cosk_vals, phi_vals
    
def fit_all_bins(all_bins,max_order):
    all_fits=[0]*len(all_bins)
    for i in range(0,len(all_bins)):
        values=make_all_fits(all_bins[i],i,max_order)
        all_fits[i]=values
        
    return all_fits


#%% testing for max_order of 5, 7 looks too much for me and we run the risk of overfitting, but play around 
all_fits=fit_all_bins(all_bins,5)

