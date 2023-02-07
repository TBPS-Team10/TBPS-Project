#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 17:37:20 2023

@author: Avi
"""

import pandas as pd
from tqdm import tqdm

def kress_filter(data):
    K_STAR_M = df['Kstar_M']
    B0_M = df['B0_M']
    B0_IPCHI2 = df['B0_IPCHI2_OWNPV']
    B0_FDCHI2 = df['B0_FDCHI2_OWNPV']
    K_STAR_0_FDCHI2 = df['Kstar_FDCHI2_OWNPV']
    end = len(B0_M) - 1
    for i in tqdm(range(0,end)):
        
        if K_STAR_M[i] < 795.9 or K_STAR_M[i] > 995.9:
            df.drop(i, axis = 0, inplace = True)
            
        if B0_M[i] < 5170 or B0_M[i] > 5700:
            df.drop(i, axis = 0, inplace = True)
      
 #       if B0_IPCHI2[i] > 16: IDENTIFY ERROR
 #          df.drop(i, axis = 0, inplace = True)
       
        if B0_FDCHI2[i] < 121:
            df.drop(i, axis = 0, inplace = True)
        
        if K_STAR_0_FDCHI2[i] < 9:
            df.drop(i, axis = 0, inplace = True)

if __name__ == "__main__":
    df = pd.read_csv("../data/total_dataset.csv")
    df.reset_index(inplace = True)

    print(kress_filter(df))