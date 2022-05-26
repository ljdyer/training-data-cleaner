from typing import Callable, Tuple

import pandas as pd

from .issues import ISSUES


# ====================
def get_diagnostic_results(df: pd.DataFrame) -> dict: 

    results = ISSUES.copy()
    new_df = df.copy()

    for issue in ISSUES.keys():
        results[issue]['num'] = get_num(df, ISSUES[issue]['mask'])
        new_df = remove(new_df, ISSUES[issue]['mask'])
        results[issue]['remaining'] = len(new_df)

    return results


# ====================
def get_num(df: pd.DataFrame, 
            mask: Callable[[pd.DataFrame], pd.Series]
            ) -> int:
    """Given a pandas dataframe and a mask function, return the number of rows
    captured when the mask is applied to the dataframe"""

    mask_ = mask(df)
    return mask_.sum()


# ====================
def keep(df: pd.DataFrame, 
         mask: Callable[[pd.DataFrame], pd.Series]
         ) -> pd.DataFrame:
    """Given a pandas dataframe and a mask function, return only the rows of the
    dataframe captured by the mask"""

    mask_ = mask(df)
    new_df = df[mask_]
    return new_df


# ====================
def remove(df: pd.DataFrame, 
           mask: Callable[[pd.DataFrame], pd.Series]
           ) -> pd.DataFrame:
    """Given a pandas dataframe and a mask function, return the dataframe that
    results when rows captured by the mask are removed"""

    mask_ = mask(df)
    new_df = df[~mask_]
    return new_df


# ====================
def get_num_and_remaining(df: pd.DataFrame, 
                          mask: Callable[[pd.DataFrame], pd.Series]
                          ) -> Tuple[int, int]:
    """Given a pandas dataframe and a mask function, return the number of rows
    captured when the mask is applied to the dataframe and the number of rows
    remaining when those rows are removed."""

    mask_ = mask(df)
    num = mask_.sum()
    remaining = len(df[~mask_])
    return num, remaining
