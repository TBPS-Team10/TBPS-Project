# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 10:40:50 2023

@author: Louis Beucher
"""

#%% fitting for bins of q2 attempting fit with Chebychev polynomial of the first kind
import  numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#create the values taken by the Chebychev polynomials
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
    
    return best_fit_params, best_cov_params, best_fit_dat, best_res_val, best_order



def make_all_fits(bin_dat,q2bin_num,max_order,plot=False):
    cosl_vals=find_best_fit(np.array(bin_dat['costhetal']),max_order)
    cosk_vals=find_best_fit(np.array(bin_dat['costhetak']),max_order)
    phi_vals=find_best_fit(np.array(bin_dat['phi']),max_order)
    if plot==True:
        plt.figure(q2bin_num)
        plt.subplot(1,3,1)
        plot_fit(bin_dat['costhetal'],cosl_vals[2],20,angular_variable=r'cos$\theta_l$')
        plt.subplot(1,3,2)
        plot_fit(bin_dat['costhetak'],cosk_vals[2],20,angular_variable=r'cos$\theta_k$')
        plt.subplot(1,3,3)
        plot_fit(bin_dat['phi'],phi_vals[2],20,angular_variable=r'$\Phi$')
        plt.suptitle(f'background fit for bin {q2bin_num}',fontweight='bold')
        plt.show()
    
    return cosl_vals, cosk_vals, phi_vals
    
def fit_all_bins(all_bins,max_order,plot=False):
    all_fits=[0]*len(all_bins)
    for i in range(0,len(all_bins)):
        values=make_all_fits(all_bins[i],i,max_order, plot=plot)
        all_fits[i]=values
        
    return all_fits


def create_background_pdf(cosl_vals,cosk_vals,phi_vals,all_fits,bin_num,ang_val=3):

    #limiting to second order Chebyshev fit because Mitesh said so
    cosl_dist=fit_Chebyshev_2(cosl_vals,all_fits[bin_num][0][0][0],all_fits[bin_num][0][0][1],all_fits[bin_num][0][0][2])
    #more complex for cosk as it might either be an exponential or a chebyshev
    
    cosk_dist=fit_Chebyshev_2(cosk_vals,all_fits[bin_num][1][0][0],all_fits[bin_num][1][0][1],all_fits[bin_num][1][0][2])
    for i in range(0,len(cosk_dist)):
        if cosk_dist[i]<0: cosk_dist[i]==0
    phi_dist=fit_Chebyshev_2(cosl_vals,all_fits[bin_num][2][0][0],all_fits[bin_num][2][0][1],all_fits[bin_num][2][0][2])
    
    return np.array(cosl_dist)*np.array(cosk_dist)*np.array(phi_dist)










    