import datetime
import os
from typing import Callable, Tuple

import numpy as np
import pandas as pd
from app_elements.exceptions import NoDataException
from flask import app, session


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


# ====================
def save_df(df: pd.DataFrame):

    session['df'] = df.to_dict()


# ====================
def drop_rows(rows_to_remove):

    df = get_df()
    df = df.drop(rows_to_remove)
    save_df(df)


# ====================
def get_df() -> pd.DataFrame:

    try:
        return pd.DataFrame(session['df'])
    except Exception as e:
        raise NoDataException


# ====================
def generate_download_fname():

    return f"{session['fname_root']}_{get_timestamp()}.{session['fname_ext']}"


# ====================
def get_download_fpath(fname):

    return os.path.join(app.config['DOWNLOAD_FOLDER'], fname)


# ====================
def get_timestamp() -> str:
    """Get a timestamp of the current time suitable for appending
    to file names"""

    return datetime.datetime.now().strftime("%d%b%Y-%H%M%S")


# ====================
def diagnose_issues(df: pd.DataFrame, issues: dict, issue_names: list) -> Tuple[list, list, int]: 

    issue_results = []
    for display_name, issue_id in issue_names:
        issue_results.append({
            **issues[issue_id],
            'issue_id': issue_id,
            'display_name': display_name,
            'num': len(keep(df, issues[issue_id]['mask']))
        })
    
    passed = [issue for issue in issue_results if issue['num'] == 0]
    failed = [issue for issue in issue_results if issue['num'] > 0]

    new_df = df.copy()
    for issue in failed:
        new_df = remove(new_df, issue['mask'])
    
    remaining = len(new_df)

    return passed, failed, remaining


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


# ====================
def read_and_preprocess(fpath: str) -> Tuple[pd.DataFrame, int]:
    """Read a dataframe from an Excel file and perform preliminary cleaning
    operations"""

    df = pd.read_excel(fpath, engine="openpyxl")
    # Fill NaN with empty strings
    df = df.fillna('')
    # Strip leading/trailing spaces
    df = df.applymap(lambda x: x.strip())
    # Remove source+target duplicates
    double_dup_mask = lambda df: df.duplicated(keep='first')
    num_double_dups = len(df[double_dup_mask])
    df = remove(df, double_dup_mask)
    # Rename source and target columns
    df.columns = ['source', 'target']

    return df, num_double_dups
