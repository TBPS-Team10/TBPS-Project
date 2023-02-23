# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 19:02:31 2023

@author: Madhuwrit Hazra
"""

import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit
from scipy.special import eval_legendre
from copy import deepcopy

class acceptance_legendre:
    def __init__(self, filtered_data, q2_bins, order_costhetal=5, order_costhetak=5, order_phi=6):
        """
        3D Legendre decompositions of the acceptance function, parameterized in
        the 3 angular variables (phi will be rescaled into the interval [-1, 1])
        in the given bins of q^2.

        Parameters
        ----------
        filtered_data : ndarray of float
            2D array of filtered acceptance_mc.csv data (acceptance function).
        q2_bins : array-like (2D)
            List/array of lists/arrays containing q^2 interval edges.
        order_costhetal : int
            Legendre expansion order in cos(theta_l). The default is 5.
        order_costhetak : int
            Legendre expansion order in cos(theta_k). The default is 5.
        order_phi : int
            Legendre expansion order in phi. The default is 6.

        Returns
        -------
        None.

        """
        self._filt_data = deepcopy(filtered_data)
        self._o_cosl = order_costhetal
        self._o_cosk = order_costhetak
        self._o_phi = order_phi
        self._q2_bins = q2_bins
        
        # 3D Legendre expansion coefficients for the different bins
        self._coeffs = np.zeros((len(q2_bins), self._o_cosl+1, self._o_cosk+1, self._o_phi+1))
        # Rescale phi into the range [-1, 1] by dividing by pi
        self.rescale_phi()
        # Perform 3D Legendre expansions
        self.expand()
        
    def rescale_phi(self):
        """
        Rescale phi so that all values lie in the interval [-1, 1] in order to
        perform a Legendre expansion of the acceptance function.

        Returns
        -------
        None.

        """
        
        self._filt_data[:,91] /= np.pi
        
    def expand(self):
        """
        Performs an unweighted Legendre expansion of the acceptance function
        in 3 dimensions (the 3 angular variables) for the given bins.

        Returns
        -------
        None.

        """
        
        for bin_num, q_bin in enumerate(self._q2_bins):
            q_min = q_bin[0]
            q_max = q_bin[1]
            # Filter self._filt_data down to the particular q^2 bin
            q_filtered = self._filt_data[q_min < self._filt_data[:,90]]
            q_filtered = q_filtered[q_filtered[:,90] < q_max]
            N = len(q_filtered)  # Number of samples in this bin
            cos_l = q_filtered[:,92]
            cos_k = q_filtered[:,93]
            phi = q_filtered[:,91]
            
            # Perform overlap integral for each permutation with the MC
            # approximation of the acceptance function
            for i in range(self._o_cosl + 1):
                integrand_cos_l = eval_legendre(i, cos_l)
                cos_l_norm = i + 0.5
                for j in range(self._o_cosk + 1):
                    integrand_cos_k = eval_legendre(j, cos_k)
                    cos_k_norm = j + 0.5
                    for k in range(self._o_phi + 1):
                        integrand_phi = eval_legendre(k, phi)
                        phi_norm = k + 0.5
                        coeff = np.sum(cos_l_norm * cos_k_norm * phi_norm *\
                                integrand_cos_l * integrand_cos_k *\
                                integrand_phi) / N
                        # Add result to the 4D matrix, self._coeffs
                        self._coeffs[bin_num, i, j, k] += coeff
                        
    def acceptance_func_cosl(self, bin_num, x):
        """
        Returns the acceptance function for cos(theta_l) at given points, x,
        in the domain [-1, 1].

        Parameters
        ----------
        bin_num : int
            q^2 bin number (indexed from 0).
        x : ndarray of float
            Points in the interval [-1, 1] to evaluate.

        Returns
        -------
        expansion : ndarray
            Acceptance function evaluated at input coordinates.

        """
        
        # Acquire Legendre expansion coefficients for the specified bin
        # and for static cos_k and phi
        # x 4 to undo the normalization constants of cos_k and phi polynomials of order 0
        coeffs = self._coeffs[bin_num, 0:, 0, 0] * 4.
        expansion = np.zeros(len(x))
        for i, coeff in enumerate(coeffs):
            # Multiply by 2 so that the function has an average of 1 (PDF; normally average of 0.5)
            expansion += coeff * eval_legendre(i, x)
            
        return expansion / np.mean(expansion)
    
    def acceptance_func_cosk(self, bin_num, x):
        """
        Returns the acceptance function for cos(theta_k) at given points, x,
        in the domain [-1, 1].

        Parameters
        ----------
        bin_num : int
            q^2 bin number (indexed from 0).
        x : ndarray of float
            Points in the interval [-1, 1] to evaluate.

        Returns
        -------
        expansion : ndarray
            Acceptance function evaluated in input coordinates.

        """
        
        # Acquire Legendre expansion coefficients for the specified bin
        # and for static cos_l and phi
        # x 4 to undo the normalization constants of cos_l and phi polynomials of order 0
        coeffs = self._coeffs[bin_num, 0, 0:, 0] * 4.
        expansion = np.zeros(len(x))
        for i, coeff in enumerate(coeffs):
            # Multiply by 2 so that the function has an average of 1 (PDF; normally average of 0.5)
            expansion += coeff * eval_legendre(i, x)
            
        return expansion / np.mean(expansion)
    
    def acceptance_func_phi(self, bin_num, x):
        """
        Returns the acceptance function for phi at given points, x,
        in the domain [-pi, pi].

        Parameters
        ----------
        bin_num : int
            q^2 bin number (indexed from 0).
        x : ndarray of float
            Points in the interval [-pi, pi] to evaluate.

        Returns
        -------
        expansion : ndarray
            Acceptance function evaluated in input coordinates.

        """
        
        # Acquire Legendre expansion coefficients for the specified bin
        # and for static cos_l and cos_k
        # x 4 to undo the normalization constants of cos_l and cos_k polynomials of order 0
        coeffs = self._coeffs[bin_num, 0, 0, 0:] * 4.
        expansion = np.zeros(len(x))
        for i, coeff in enumerate(coeffs):
            # Multiply by 2 so that the function has an average of 1 (PDF; normally average of 0.5)
            # Divide by pi to transform the domain to [-1, 1]
            expansion += coeff * eval_legendre(i, x / np.pi)
            
        return expansion / np.mean(expansion)
    
    def acceptance_func(self, bin_num, cos_l, cos_k, phi):
        # Acquire Legendre expansion acceptance function values
        # 3D array of coefficients
        coeffs = self._coeffs[bin_num]
        # cos_l, cos_k and phi should all have the same length
        expansion = np.zeros(len(cos_l))
        
        for i in range(self._o_cosl + 1):
            legendre_cos_l = eval_legendre(i, cos_l)
            for j in range(self._o_cosk + 1):
                legendre_cos_k = eval_legendre(j, cos_k)
                for k in range(self._o_phi + 1):
                    # Divide by pi to transform to the range [-1, 1]
                    legendre_phi = eval_legendre(k, phi / np.pi)
                    expansion += coeffs[i,j,k] * legendre_cos_l * legendre_cos_k *\
                        legendre_phi
        
        # Return with a mean of 1 for convenience
        return expansion / np.mean(expansion)
    
    def plot_acceptance_cosl(self, bin_num):
        """
        Plot acceptance function for a particular bin in terms of cos(theta_l).

        Parameters
        ----------
        bin_num : int
            q^2 bin number to plot, indexed from 0.

        Returns
        -------
        None.

        """
        
        q_min = self._q2_bins[bin_num][0]
        q_max = self._q2_bins[bin_num][1]
        q_filtered = self._filt_data[q_min < self._filt_data[:,90]]
        q_filtered = q_filtered[q_filtered[:,90] < q_max]
        
        # Acquire Legendre expansion coefficients for the specified bin
        # and for static cos_k and phi
        # x 4 to undo the normalization constants of cos_k and phi polynomials of order 0
        coeffs = self._coeffs[bin_num, 0:, 0, 0] * 4.
        x = np.linspace(-1., 1., 200)
        expansion = np.zeros(200)
        
        for i, coeff in enumerate(coeffs):
            expansion += coeff * eval_legendre(i, x) 
        
        plt.title(r"cos($\theta_{l}$) Acceptance Legendre Expansion (%.ith order)" % (i))
        plt.hist(q_filtered[:,92], bins=50, range=[-1., 1.], color="orange", alpha=0.5, density=True)
        plt.plot(x, expansion, color="blue")
        plt.xlabel(r"cos($\theta_{l}$)")
        plt.ylabel("Acceptance function / 2")
        plt.grid()
        plt.show()
        
    def plot_acceptance_cosk(self, bin_num):
        """
        Plot acceptance function for a particular bin in terms of cos(theta_k).

        Parameters
        ----------
        bin_num : int
            q^2 bin number to plot, indexed from 0.

        Returns
        -------
        None.

        """
        
        q_min = self._q2_bins[bin_num][0]
        q_max = self._q2_bins[bin_num][1]
        q_filtered = self._filt_data[q_min < self._filt_data[:,90]]
        q_filtered = q_filtered[q_filtered[:,90] < q_max]
        
        # Acquire Legendre expansion coefficients for the specified bin
        # and for static cos_l and phi
        # x 4 to undo the normalization constants of cos_l and phi polynomials of order 0
        coeffs = self._coeffs[bin_num, 0, 0:, 0] * 4.
        x = np.linspace(-1., 1., 200)
        expansion = np.zeros(200)
        
        for i, coeff in enumerate(coeffs):
            expansion += coeff * eval_legendre(i, x) 
        
        plt.title(r"cos($\theta_{k}$) Acceptance Legendre Expansion (%.ith order)" % (i))
        plt.hist(q_filtered[:,93], bins=50, range=[-1., 1.], color="orange", alpha=0.5, density=True)
        plt.plot(x, expansion, color="blue")
        plt.xlabel(r"cos($\theta_{k}$)")
        plt.ylabel("Acceptance function / 2")
        plt.grid()
        plt.show()
    
    def plot_acceptance_phi(self, bin_num):
        """
        Plot acceptance function for a particular bin in terms of phi.

        Parameters
        ----------
        bin_num : int
            q^2 bin number to plot, indexed from 0.

        Returns
        -------
        None.

        """
        
        q_min = self._q2_bins[bin_num][0]
        q_max = self._q2_bins[bin_num][1]
        q_filtered = self._filt_data[q_min < self._filt_data[:,90]]
        q_filtered = q_filtered[q_filtered[:,90] < q_max]
        
        # Acquire Legendre expansion coefficients for the specified bin
        # and for static cos_l and cos_k
        # x 4 to undo the normalization constants of cos_l and cos_k polynomials of order 0
        coeffs = self._coeffs[bin_num, 0, 0, 0:] * 4.
        x = np.linspace(-1., 1., 200)
        expansion = np.zeros(200)
        
        for i, coeff in enumerate(coeffs):
            expansion += coeff * eval_legendre(i, x) 
        
        plt.title(r"cos($\phi$) Acceptance Legendre Expansion (%.ith order)" % (i))
        plt.hist(q_filtered[:,91], bins=50, range=[-1., 1.], color="orange", alpha=0.5, density=True)
        plt.plot(x, expansion, color="blue")
        plt.xlabel(r"$\phi/\pi$")
        plt.ylabel("Acceptance function")
        plt.grid()
        plt.show()
        
    def fit_cos_l_func(self, data, bin_num):
        """
        Fits the 1D PDF given at the start of the project in a given bin.
        Exists largely for debug purposes; may be better to use
        fit_SM_observables().

        Parameters
        ----------
        data : ndarray
            Filtered signal data.
        bin_num : int
            Bin number (index) to fit in.

        Returns
        -------
        list
            List of F_L, A_FB and associated estimated errors from iminuit.

        """
        q_min = self._q2_bins[bin_num][0]
        q_max = self._q2_bins[bin_num][1]
        q_filtered = data[q_min < data[:,90]]
        q_filtered = q_filtered[q_filtered[:,90] < q_max]
        
        cos_l = q_filtered[:,92]
        acceptance = self.acceptance_func_cosl(bin_num, cos_l)
        
        def cos_l_func(F_L, A_FB):
            cos_2l = 2. * cos_l**2 - 1.
            return (3./8.) * (1.5 - 0.5*F_L + 0.5*cos_2l*(1. - 3.*F_L) + (8./3.)*A_FB*cos_l)
                
        def cos_l_func_NLL(F_L, A_FB):
            func_values = cos_l_func(F_L, A_FB) * acceptance
            return -1. * np.sum(np.log(func_values))
        
        cos_l_func_NLL.errordef = Minuit.LIKELIHOOD
        minimizer = Minuit(cos_l_func_NLL, F_L = 0.3, A_FB = 0.)
        minimizer.limits=((-3., 3.), (-1., 1.))
        minimizer.migrad()
        minimizer.hesse()
        
        # Store the fitted parameters and associated errors
        F_L = minimizer.values[0]
        F_L_error = minimizer.errors[0]
        A_FB = minimizer.values[1]
        A_FB_error = minimizer.errors[1]
        
        print("Valid function minumum: " + str(minimizer.fmin.is_valid))
        
        # Reassign to this for the sake of plotting the fit
        cos_l = np.linspace(-1., 1., 200)
        
        """
        plt.title(r"Bin %.i ($F_{L}=%.2f$, $A_{FB}=%.2f$)" % (bin_num, F_L, A_FB))
        plt.hist(q_filtered[:,92], bins=25, range=[-1., 1.], density="True", color="orange", alpha=0.5)
        plt.plot(cos_l, cos_l_func(F_L, A_FB)*self.acceptance_func_cosl(bin_num, np.linspace(-1., 1., 200)), color="blue")
        plt.xlabel(r"cos($\theta_{l}$)")
        plt.ylabel("Normalized candidate distribution")
        plt.grid(True)
        plt.show()
        """
        
        return [F_L, F_L_error, A_FB, A_FB_error]
    
    def fit_SM_observables(self, data, bin_num):
        """
        Fits the 3D PDF (see literature) for a given bin with an NLL minimizer.

        Parameters
        ----------
        data : ndarray
            Filtered signal data.
        bin_num : int
            Bin number (index) to fit in.

        Returns
        -------
        ndarray
            Array of SM parameters with estimated errors from iminuit minimizer.

        """
        q_min = self._q2_bins[bin_num][0]
        q_max = self._q2_bins[bin_num][1]
        q_filtered = data[q_min < data[:,90]]
        q_filtered = q_filtered[q_filtered[:,90] < q_max]
        
        cos_l = q_filtered[:,92]
        cos_k = q_filtered[:,93]
        phi = q_filtered[:,91]
        acceptance = self.acceptance_func(bin_num, cos_l, cos_k, phi)
        # Remove negative values because they'll inherently impede an NLL
        # minimization function (unlikely to occur, but just in case)
        positive_vals = acceptance > 0.
        cos_l = cos_l[positive_vals]
        cos_k = cos_k[positive_vals]
        phi = phi[positive_vals]
        acceptance = acceptance[positive_vals]
        
        cos_squared_k = cos_k**2
        cos_2l = 2. * cos_l**2 - 1.
        cos_phi = np.cos(phi)
        cos_2phi = np.cos(2. * phi)
        
        sin_squared_l = 1. - cos_l**2
        sin_squared_k = 1. - cos_squared_k
        sin_l = np.sqrt(sin_squared_l)
        sin_k = np.sqrt(sin_squared_k)
        sin_2l = 2. * sin_l * cos_l
        sin_2k = 2. * sin_k * cos_k
        sin_phi = np.sin(phi)
        sin_2phi = np.sin(2. * phi)
        
        # Yes, functions inside functions inside classes...
        def PDF(F_L, A_FB, S3, S4, S5, S7, S8, S9):
            func_vals = 0.75 * (1. - F_L) * sin_squared_k
            func_vals += F_L * cos_squared_k
            func_vals += 0.25 * (1. - F_L) * sin_squared_k * cos_2l
            func_vals -= F_L * cos_squared_k * cos_2l
            func_vals += S3 * sin_squared_k * sin_squared_l * cos_2phi
            func_vals += S4 * sin_2k * sin_2l * cos_phi
            func_vals += S5 * sin_2k * sin_l * cos_phi
            func_vals += (4./3.) * A_FB * sin_squared_k * cos_l
            func_vals += S7 * sin_2k * sin_l * sin_phi
            func_vals += S8 * sin_2k * sin_2l * sin_phi
            func_vals += S9 * sin_squared_k * sin_squared_l * sin_2phi
            func_vals *= (9./32.) * np.pi
            func_vals *= acceptance
            return func_vals
        
        def PDF_NLL(F_L, A_FB, S3, S4, S5, S7, S8, S9):
            func_vals = PDF(F_L, A_FB, S3, S4, S5, S7, S8, S9)
            return -1. * np.sum(np.log(func_vals))
        
        PDF_NLL.errordef = Minuit.LIKELIHOOD
        minimizer = Minuit(PDF_NLL, F_L=0.3, A_FB=0., S3=0., S4=0., S5=0., S7=0., S8=0., S9=0.)
        minimizer.limits=((-1., 1.), (-1., 1.), (-1., 1.), (-1., 1.), (-1., 1.),\
                          (-1., 1.), (-1., 1.), (-1., 1.))
        minimizer.migrad()
        minimizer.hesse()
        
        # Store the fitted parameters and associated errors
        F_L = minimizer.values[0]
        F_L_error = minimizer.errors[0]
        A_FB = minimizer.values[1]
        A_FB_error = minimizer.errors[1]
        S3 = minimizer.values[2]
        S3_error = minimizer.errors[2]
        S4 = minimizer.values[3]
        S4_error = minimizer.errors[3]
        S5 = minimizer.values[4]
        S5_error = minimizer.errors[4]
        S7 = minimizer.values[5]
        S7_error = minimizer.errors[5]
        S8 = minimizer.values[6]
        S8_error = minimizer.errors[6]
        S9 = minimizer.values[7]
        S9_error = minimizer.errors[7]
        
        #minimizer.draw_mnprofile("S7", bound=5)
        
        print("Valid function minumum: " + str(minimizer.fmin.is_valid))
        
        return np.array([[F_L, F_L_error], [A_FB, A_FB_error], [S3, S3_error],\
                         [S4, S4_error], [S5, S5_error], [S7, S7_error], [S8, S8_error],\
                         [S9, S9_error]])