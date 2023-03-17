#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 13:12:01 2023

@author: emilyip
"""

def chi_sq(datax,datay,dataerr,theoy):
  '''
  Chi square test which should take into account the error of the data points
  Requires datax (x),datay(y) and dataerr (y error) for data, theoy is theoretical distribution f(datax)
  returns the ration, if it fits the theoretical distribution the ratio should be ~1
  '''
  chi_sq_sum = 0.0;
  for i in range(len(datax)):
    x = datax[i]
    y = datay[i]
    err = dataerr[i]
    y_act = theoy[i]
    chi_sq_sum += ((y_act-y)/(err))**2
  N_dof = len(datax)-1;
  return chi_sq_sum/N_dof