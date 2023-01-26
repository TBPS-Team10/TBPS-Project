import pandas as pd
from pathlib import Path

if __name__ == "__main__":
    # This is how you can load data from the data directory, assuming the script
    # being run is located directly within src/. If it is in a subfolder, you
    # will need to call an extra .parent from the Path object.
    DATADIR = Path(__file__).parent.parent / 'data'
    df = pd.read_csv(DATADIR / "total_dataset.csv") # Note the / operator used
    print(df)