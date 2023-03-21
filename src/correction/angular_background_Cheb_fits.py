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

def bin_separation_array(dat):
    bin_0=dat[dat[:,90]>=0.1]
    bin_0=bin_0[bin_0[:,90]<=0.98]
    bin_1=dat[dat[:,90]>=1.1]
    bin_1=bin_1[bin_1[:,90]<=2.5]
    bin_2=dat[dat[:,90]>2.5]
    bin_2=bin_2[bin_2[:,90]<=4.0]
    bin_3=dat[dat[:,90]>4.0]
    bin_3=bin_3[bin_3[:,90]<=6.0]
    bin_4=dat[dat[:,90]>6.0]
    bin_4=bin_4[bin_4[:,90]<=8.0]
    bin_5=dat[dat[:,90]>=15.0]
    bin_5=bin_5[bin_5[:,90]<=17.0]
    bin_6=dat[dat[:,90]>17.0]
    bin_6=bin_6[bin_6[:,90]<=19.0]
    bin_7=dat[dat[:,90]>=11.0]
    bin_7=bin_7[bin_7[:,90]<=12.5]
    bin_8=dat[dat[:,90]>1.0]
    bin_8=bin_8[bin_8[:,90]<=6.0]
    bin_9=dat[dat[:,90]>=15.0]
    bin_9=bin_9[bin_9[:,90]<=19.0]
    
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

    
def bin_mid(bin_edges):
    #return the coordinate of the middle of the bin rather than its edges
    bin_mid=[]
    for i in range(0,len(bin_edges)-1):
        bin_mid.append((bin_edges[i]+bin_edges[i+1])/2)
    
    return bin_mid
    

def plot_fit(angle_data,fit_dat,bins,angular_variable=r'cos$\theta_k$'):
    freq,bin_edges=np.histogram(angle_data,bins=bins,density=True)
    freq2,_=np.histogram(angle_data,bins=bins,density=False)
    yerr=np.sqrt(freq2)*(freq/freq2)
    x_dat=bin_mid(bin_edges)
    x_dat2=np.linspace(bin_edges[0],bin_edges[-1],100)
    xerr=(bin_edges[-1]-bin_edges[0])/10
    plt.errorbar(x_dat,freq,xerr=xerr,yerr=yerr,fmt='o',color='black',capsize=2.0,label='simulated data')
    plt.plot(x_dat,fit_dat,color='darkred',label='fit data')
    plt.xlabel(angular_variable)
    plt.ylabel('frequency')
    #plt.legend()
    plt.tight_layout()
    
    
def make_fit_Chebyshev(angle_data,max_order):
    freq,bin_edges=np.histogram(angle_data,bins=10,density=True)
    x_dat=bin_mid(bin_edges)
    #starting with a flat initial guess and praying for the best
    initial_guess=0.2*np.ones(max_order+1)
    fit_params,cov_params=curve_fit(fit_Chebyshev_2,x_dat,freq,p0=initial_guess)
    x_dat2=np.linspace(bin_edges[0],bin_edges[-1],100)
    fit_dat=fit_Chebyshev_2(x_dat,*fit_params)
    
    return fit_params, cov_params, fit_dat

def make_all_fits(bin_dat,q2bin_num,max_order,plot=False):
    cosl_vals=make_fit_Chebyshev(np.array(bin_dat['costhetal']),max_order)
    cosk_vals=make_fit_Chebyshev(np.array(bin_dat['costhetak']),max_order)
    phi_vals=make_fit_Chebyshev(np.array(bin_dat['phi']),max_order)
    if plot==True:
        plt.figure(q2bin_num)
        #plt.subplot(1,3,1)
        plot_fit(bin_dat['costhetal'],cosl_vals[2],10,angular_variable=r'cos$\theta_l$')
        #plt.subplot(1,3,2)
        #plot_fit(bin_dat['costhetak'],cosk_vals[2],10,angular_variable=r'cos$\theta_k$')
        #plt.subplot(1,3,3)
        #plot_fit(bin_dat['phi'],phi_vals[2],10,angular_variable=r'$\Phi$')
        #plt.suptitle(f'background fit for bin {q2bin_num}',fontweight='bold')
        
        #plt.savefig(f"figures/new_Cheb/CheB_fit_bin_{q2bin_num}.svg", format="svg")
        plt.show()
    
    fit_params= cosl_vals, cosk_vals, phi_vals
    return fit_params
    
def fit_all_bins(all_bins,max_order,plot=False):
    all_fits=[0]*len(all_bins)
    for i in range(0,len(all_bins)):
        values=make_all_fits(all_bins[i],i,max_order, plot=plot)
        all_fits[i]=values
        
    return all_fits


def create_background_pdf(cosl_vals,cosk_vals,phi_vals,all_fits,bin_num):

    #limiting to second order Chebyshev fit because Mitesh said so
    cosl_dist=fit_Chebyshev_2(cosl_vals,all_fits[bin_num][0][0][0],all_fits[bin_num][0][0][1],all_fits[bin_num][0][0][2])
    cosk_dist=fit_Chebyshev_2(cosk_vals,all_fits[bin_num][1][0][0],all_fits[bin_num][1][0][1],all_fits[bin_num][1][0][2])
    phi_dist=fit_Chebyshev_2(cosl_vals,all_fits[bin_num][2][0][0],all_fits[bin_num][2][0][1],all_fits[bin_num][2][0][2])
    
    #set to 0 if pdf gets negative
    for i in range(0,len(cosk_dist)):
        if cosl_dist[i]<0: cosk_dist[i]==0
        if cosk_dist[i]<0: cosk_dist[i]==0
        if phi_dist[i]<0: phi_dist[i]==0
        
    return np.array(cosl_dist)*np.array(cosk_dist)*np.array(phi_dist)

def create_background_mesh(cosl_val, cosk_mesh, phi_mesh, all_fits, bin_num):
    
    cosl_dist=fit_Chebyshev_2(np.array([cosl_val]),all_fits[bin_num][0][0][0],all_fits[bin_num][0][0][1],all_fits[bin_num][0][0][2])
    
    cosk_dist=np.zeros((len(cosk_mesh),len(cosk_mesh)))
    for i in range(0,len(cosk_mesh)):
        cosk_dist[:,i]=fit_Chebyshev_2(cosk_mesh[:,i],all_fits[bin_num][1][0][0],all_fits[bin_num][1][0][1],all_fits[bin_num][1][0][2])
    
    phi_dist=np.zeros((len(phi_mesh),len(phi_mesh)))
    for i in range(0,len(phi_mesh)):
        phi_dist[:,i]=fit_Chebyshev_2(phi_mesh[:,i],all_fits[bin_num][2][0][0],all_fits[bin_num][2][0][1],all_fits[bin_num][2][0][2])

    background_PDF=cosl_dist*cosk_dist*phi_dist
    
    return background_PDF




    