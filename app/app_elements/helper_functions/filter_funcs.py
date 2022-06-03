"""
issue_functions.py
"""

from flask import current_app
import pandas as pd
from app_elements.helper_functions.helper import *


# ====================
def mask_none(df: pd.DataFrame) -> pd.Series:

    return df.apply(lambda x: True, axis=1)


# ====================
def mask_empty(col: pd.Series) -> pd.Series:

    return col.apply(lambda x: x == '')


# ====================
def mask_same(df: pd.DataFrame) -> pd.Series:

    return df.apply(lambda x: x['source'] == x['target'], axis=1)


# ====================
def mask_too_long(col: pd.Series) -> pd.Series:

    return col.apply(lambda x: len(x) > current_app.config['MAX_NUM_CHARS'])
