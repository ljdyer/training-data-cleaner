"""
html_helper.py

Helper functions to generate dataframes from other dataframes
"""

import pandas as pd
import numpy as np


# ====================
def get_source_dup_df(df: pd.DataFrame, skipped_sources) -> pd.DataFrame:
    """Get a dataframe with all source dupes from a pandas dataframe"""

    df_out = df[df[df.columns[0]].apply(
        lambda x, s=skipped_sources: False if x in s else True)]
    df_out = (
        df_out[df_out.duplicated(subset=[df_out.columns[0]], keep=False)]
        .sort_values(df_out.columns[0]).reset_index()
    )
    df_out = (df_out.rename(columns={'index': 'orig_index'}).fillna(''))
    return df_out


# ====================
def read_df_from_excel(df_path: str) -> pd.DataFrame:
    """Read a dataframe from an Excel file and perform preliminary cleaning
    operations"""

    df = pd.read_excel(df_path, engine="openpyxl")
    df = df.fillna('')
    df = df.applymap(lambda x: x.strip())
    return df


# ====================
def get_first_dup_df(all_source_dup_df: pd.DataFrame,
                     source_column: str, target_column: str):
    """Get a dataframe with the first duplicate group from a pandas
    dataframe"""

    this_source = all_source_dup_df.iloc[0][source_column]
    first_dup_df = all_source_dup_df[
        all_source_dup_df[source_column] == this_source]
    # Reorder columns
    first_dup_df = first_dup_df[['orig_index', source_column, target_column]]
    first_dup_df.index = np.arange(1, len(first_dup_df) + 1)
    return first_dup_df, this_source
