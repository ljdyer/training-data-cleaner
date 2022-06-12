import pandas as pd
from app_elements.exceptions import NoDataException
from flask import session


# ====================
def save_df(df: pd.DataFrame):
    """Save the current main dataframe to the current session as a
    dictionary"""

    session['df'] = df.to_dict()


# ====================
def save_preview_df(df: pd.DataFrame):
    """Save the current preview dataframe to the current session
    as a dictionary"""

    session['preview_df'] = df.to_dict()


# ====================
def drop_rows(rows_to_remove: list):
    """Drop rows from the currently saved dataframe"""

    df = get_df()
    df = df.drop(rows_to_remove)
    save_df(df)


# ====================
def get_df() -> pd.DataFrame:
    """Get the currently saved main dataframe as a pandas dataframe"""

    try:
        return pd.DataFrame(session['df'])
    except KeyError:
        raise NoDataException


# ====================
def check_df_in_session():
    """Check that the current session has the 'df' key"""

    if 'df' not in session:
        raise NoDataException


# ====================
def get_preview_df() -> pd.DataFrame:
    """Get the current preview dataframe"""

    return pd.DataFrame(session['preview_df'])
