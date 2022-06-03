import pandas as pd

def sort_key_length(col: pd.Series) -> pd.Series:

    return col.str.len()


def sort_key_ratio(df: pd.DataFrame) -> pd.Series:

    len_source = df['source'].str.len()
    len_target = df['target'].str.len()
    # Smoothing to avoid zero division
    len_target = len_target.apply(lambda x: 0.01 if x == 0 else x)
    ratio = len_source.div(len_target)    
    return ratio


def sort_key_index(df: pd.DataFrame) -> pd.Series:

    return df.index