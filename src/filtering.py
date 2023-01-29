import pandas as pd
from tqdm import tqdm

if __name__ == "__main__":
    df = pd.read_csv("../data/total_dataset.csv")

def parkinson_filter(data):
    k_star = df['Kstar_M']
    B0 = df['B0_M']
    
    for i in tqdm(range(0,len(k_star)-1)):
        
        if k_star[i] < 792 or k_star[i] > 992:
            df.drop(i, axis = 0, inplace = True)
            
        if B0[i] < 4850 or B0[i] > 5780:
            df.drop(i, axis = 0, inplace = True)
            
    df.reset_index(inplace = True)
