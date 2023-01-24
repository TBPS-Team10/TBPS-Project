import pandas as pd

if __name__ == "__main__":
    # This is how you can load data from the data directory, note the '.' leading the file path. 
    # This is used to navigate one directory higher, out of the src/ directory and into the root.
    df = pd.read_csv("./data/total_dataset.csv")