import datetime
import os
from typing import Callable, Tuple

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
    print(issue_results)
    
    passed = [issue for issue in issue_results if issue['num'] == 0]
    failed = [issue for issue in issue_results if issue['num'] > 0]

    new_df = df.copy()
    for issue in failed:
        new_df = remove(new_df, issue['mask'])
    
    remaining = len(new_df)

    return passed, failed, remaining