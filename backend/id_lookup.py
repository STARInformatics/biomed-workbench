import os
from typing import Optional
import pandas as pd

path = os.path.join('backend', 'data', 'id_mapping.csv')

df = None

def load():
    global df

    if df is None:
        df = pd.read_csv(path, sep='\t')

    return df

def id_lookup(name:str) -> Optional[str]:
    df = load()
    df = df[df['name'] == name]

    if df.empty:
        return None
    else:
        return df.iloc[0]['id']
