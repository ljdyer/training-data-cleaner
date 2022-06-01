import pandas as pd

def sort_key_length(col: pd.Series) -> pd.Series:

    return col.str.len()


def sort_key_ratio(df: pd.DataFrame) -> pd.Series:

    return df.apply(lambda x: len(x['source'])/len(x['target']))