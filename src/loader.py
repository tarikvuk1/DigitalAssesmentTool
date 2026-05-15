import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    return pd.read_excel(path, header=1)