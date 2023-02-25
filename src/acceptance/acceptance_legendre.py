# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 19:02:31 2023

@author: Madhuwrit Hazra
"""

import numpy as np
import pandas as pd
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
        # 3D array of coefficients for the given bin number
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
        Not recommended—use fit_SM_observables_bootstrap() instead. This
        function is kept largely for documentation purposes.

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
        Not recommended—use fit_SM_observables_bootstrap() instead. This
        function is kept largely for documentation purposes.

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
            
    def fit_SM_observables_bootstrap(self, data, bootstrap_number=1000):
        """
        Fits the 3D PDF (see literature) in all bins with an NLL minimizer and
        a bootstrapping process.

        Parameters
        ----------
        data : ndarray
            Filtered signal data.
        bootstrap_number : int, optional
            Number of bootstrapping samples. The default is 1000.

        Returns
        -------
        None

        """
        # Stores all bootstrapped values of the 8 parameters
        bootstrap_parameters = np.zeros((len(self._q2_bins), bootstrap_number, 8)).astype("float32")
        
        for bin_num in range(len(self._q2_bins)):
            q_min = self._q2_bins[bin_num][0]
            q_max = self._q2_bins[bin_num][1]
            q_filtered = data[q_min < data[:,90]]
            q_filtered = q_filtered[q_filtered[:,90] < q_max]
            
            cos_l = q_filtered[:,92]
            cos_k = q_filtered[:,93]
            phi = q_filtered[:,91]
            acceptance = self.acceptance_func(bin_num, cos_l, cos_k, phi)
            # Remove negative values because they'll inherently impede an NLL
            # minimization function (should be avoided, but just in case)
            positive_vals = acceptance > 0.
            cos_l = cos_l[positive_vals]
            cos_k = cos_k[positive_vals]
            phi = phi[positive_vals]
            acceptance = acceptance[positive_vals]
            del positive_vals
            
            # Total number of remaining events
            N = len(cos_l)
            
            # Bootstrapping can pick from these with replacement
            sample_numbers = np.arange(N)
            
            for i in range(bootstrap_number):
                # Pick N random samples with replacement
                sample_indices = np.random.choice(sample_numbers, N)
                sample_cos_l = np.zeros(N)
                sample_cos_k = np.zeros(N)
                sample_phi = np.zeros(N)
                sample_acceptance = np.zeros(N)
                # Populate with bootstrap samples
                for j, index in enumerate(sample_indices):
                    sample_cos_l[j] = cos_l[index]
                    sample_cos_k[j] = cos_k[index]
                    sample_phi[j] = phi[index]
                    sample_acceptance[j] = acceptance[index]
                    
                cos_squared_k = sample_cos_k**2
                cos_2l = 2. * sample_cos_l**2 - 1.
                cos_phi = np.cos(sample_phi)
                cos_2phi = np.cos(2. * sample_phi)
                
                sin_squared_l = 1. - sample_cos_l**2
                sin_squared_k = 1. - cos_squared_k
                sin_l = np.sqrt(sin_squared_l)
                sin_k = np.sqrt(sin_squared_k)
                sin_2l = 2. * sin_l * sample_cos_l
                sin_2k = 2. * sin_k * sample_cos_k
                sin_phi = np.sin(sample_phi)
                sin_2phi = np.sin(2. * sample_phi)
                
                def PDF(F_L, A_FB, S3, S4, S5, S7, S8, S9):
                    func_vals = 0.75 * (1. - F_L) * sin_squared_k
                    func_vals += F_L * cos_squared_k
                    func_vals += 0.25 * (1. - F_L) * sin_squared_k * cos_2l
                    func_vals -= F_L * cos_squared_k * cos_2l
                    func_vals += S3 * sin_squared_k * sin_squared_l * cos_2phi
                    func_vals += S4 * sin_2k * sin_2l * cos_phi
                    func_vals += S5 * sin_2k * sin_l * cos_phi
                    func_vals += (4./3.) * A_FB * sin_squared_k * sample_cos_l
                    func_vals += S7 * sin_2k * sin_l * sin_phi
                    func_vals += S8 * sin_2k * sin_2l * sin_phi
                    func_vals += S9 * sin_squared_k * sin_squared_l * sin_2phi
                    func_vals *= sample_acceptance
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
                
                # Store the fitted parameters
                F_L = minimizer.values[0]
                A_FB = minimizer.values[1]
                S3 = minimizer.values[2]
                S4 = minimizer.values[3]
                S5 = minimizer.values[4]
                S7 = minimizer.values[5]
                S8 = minimizer.values[6]
                S9 = minimizer.values[7]
                
                values = np.zeros(8)
                values = np.array([F_L, A_FB, S3, S4, S5, S7, S8, S9])
                bootstrap_parameters[bin_num, i] += values
                
            print("Bin %.i complete (debug purposes)" % (bin_num))
            
        # Store the final result for the parameters and errors
        self._SM_parameters = np.zeros((10, 8))
        self._SM_parameter_errors = np.zeros((10, 8))
        
        # Iterate through each bin to get the needed parameters
        for i, bin_data in enumerate(bootstrap_parameters):
            self._SM_parameters[i] += np.mean(bin_data, axis=0)
            self._SM_parameter_errors[i] += np.std(bin_data, axis=0)
            
    def return_SM_observables(self):
        """
        Returns fitted SM observables. Must be run after
        fit_SM_observables_bootstrap()!

        Returns
        -------
        DataFrame
            Array of fitted SM observables in each bin. Rows correspond to bins
            and columns to observables.

        """
        variables = ["F_L", "A_FB", "S_3", "S_4", "S_5", "S_7",\
                           "S_8", "S_9"]
        return pd.DataFrame(self._SM_parameters, columns=variables)
    
    def return_SM_observables_errors(self):
        """
        Returns errors on fitted SM observables. Must be run after
        fit_SM_observables_bootstrap()!

        Returns
        -------
        DataFrame
            Array of errors on fitted SM observables in each bin. Rows correspond
            to bins and columns to observables.

        """
        variables = ["F_L", "A_FB", "S_3", "S_4", "S_5", "S_7",\
                           "S_8", "S_9"]
        return pd.DataFrame(self._SM_parameter_errors, columns=variables)
            
    def plot_SM_observables(self, observable_number, SM_predictions, SM_predictions_errors):
        """
        Plots fitted SM observables and SM predictions. The function
        fit_SM_observables_bootstrap() must be run first!

        Parameters
        ----------
        observable_number : int
            Defines which observable to plot as follows:
                0 = F_L
                1 = A_FB
                2 = S3
                3 = S4
                4 = S5
                5 = S7
                6 = S8
                7 = S9

        Returns
        -------
        None.

        """
        parameter_names = ["F_{L}", "A_{FB}", "S_{3}", "S_{4}", "S_{5}", "S_{7}",\
                           "S_{8}", "S_{9}"]
        bin_centres = [np.mean(x) for x in self._q2_bins]
        bin_widths = [0.5 * (x[1] - x[0]) for x in self._q2_bins]
        
        name = parameter_names[observable_number]
        observables = self._SM_parameters[:,observable_number]
        errors = self._SM_parameter_errors[:,observable_number]
        
        plt.title(r"$" + name + "$", fontsize=16)
        plt.plot(bin_centres, observables, "x", color="blue", ms=10, label=r"$" + name + "$")
        plt.errorbar(bin_centres, observables, xerr=bin_widths, yerr=errors, color="blue", fmt=".k", capsize=7)
        
        # Don't plot the 2 wide bins (they overlap with other bins)
        predictions = SM_predictions[:,observable_number][:-2]
        prediction_errors = SM_predictions_errors[:,observable_number][:-2]
        for i in range(len(predictions) - 1):
            x = [bin_centres[i] - bin_widths[i], bin_centres[i] + bin_widths[i]]
            y_1 = [predictions[i] + prediction_errors[i], predictions[i] + prediction_errors[i]]
            y_2 = [predictions[i] - prediction_errors[i], predictions[i] - prediction_errors[i]]
            plt.fill_between(x, y_1, y_2, color="red", alpha=0.3)
            
        x = [bin_centres[7] - bin_widths[7], bin_centres[7] + bin_widths[7]]
        y_1 = [predictions[7] + prediction_errors[7], predictions[7] + prediction_errors[7]]
        y_2 = [predictions[7] - prediction_errors[7], predictions[7] - prediction_errors[7]]
        plt.fill_between(x, y_1, y_2, color="red", alpha=0.3, label="SM predictions")
        
        plt.xlabel(r"$q^{2}$ (GeV$^{2}$/$c^{4}$)")
        plt.ylabel(r"$" + name + "$")
        plt.grid(True)
        plt.legend()
        plt.show()