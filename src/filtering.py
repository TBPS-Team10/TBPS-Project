import numpy as np
import pandas as pd
from tqdm import tqdm
data = pd.read_csv('total_dataset.csv')
def parkinson_filter(data):
    k_star = data['Kstar_M']
    B0 = data[B0_M]
    for i in tqdm(range(0,len(k_star)-1)):
        if k_star[i] < 792 or k_star[i] > 992:
            data.drop(i, axis = 0, inplace = True)
        if B0[i] < 4850 or B0[i] > 5780:
            data.drop(i, axis = 0, inplace = True)
    data.reset_index(inplace = True)
data = parkinson_mass_filter(data)

