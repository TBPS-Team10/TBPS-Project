import pandas as pd
from pathlib import Path

if __name__ == "__main__":
    df = pd.read_csv("../data/total_dataset.csv") # "../" has been used to go up one directory
    print(df)