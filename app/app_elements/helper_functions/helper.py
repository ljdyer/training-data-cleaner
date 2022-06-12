import pandas as pd
from app_elements.exceptions import NoDataException
from flask import session


# ====================
def mask_source_dup(df: pd.DataFrame) -> pd.Series:
    """Mask to capture duplicated source texts in a pandas dataframe"""

    return df.duplicated(subset=['source'])


# ====================
def save_df(df: pd.DataFrame):

    session['df'] = df.to_dict()


# ====================
def save_preview_df(df: pd.DataFrame):

    session['preview_df'] = df.to_dict()


# ====================
def drop_rows(rows_to_remove):

    df = get_df()
    df = df.drop(rows_to_remove)
    save_df(df)


# ====================
def get_df() -> pd.DataFrame:

    try:
        return pd.DataFrame(session['df'])
    except KeyError:
        raise NoDataException


# ====================
def check_df_in_session():

    if 'df' not in session:
        raise NoDataException


# ====================
def get_preview_df() -> pd.DataFrame:

    return pd.DataFrame(session['preview_df'])
