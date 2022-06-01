"""
issue_functions.py
"""

import pandas as pd
from helpers.helper import *

ACTION_SELECT_ALL = {
    'id': 'select_all',
    'text': 'Select all',
    'shortcut': 'a',
    'class': 'btn-success',
}

ACTION_DESELECT_ALL = {
    'id': 'deselect_all',
    'text': 'Deselect all',
    'shortcut': 'd',
    'class': 'btn-danger'
}

ACTION_SKIP = {
    'id': 'skip',
    'text': 'Skip this page',
    'shortcut': 's',
    'class': 'btn-primary'
}

ACTION_SUBMIT = {
    'id': 'submit',
    'text': 'Save changes & remove selected',
    'shortcut': 'enter',
    'class': 'btn-primary'
}

ACTION_REMOVE_ALL_DUPLICATES = {
    'id': 'remove_all',
    'text': 'Remove all duplicates',
    'shortcut': 'x',
    'class': 'btn-danger'
}


# === EMPTY ===

# ====================
def mask_none(col: pd.Series) -> pd.Series:

    return col.apply(lambda x: True)


# ====================
def mask_empty(col: pd.DataFrame) -> pd.Series:

    return col.apply(lambda x: x == '')


# ====================
def mask_same(df: pd.DataFrame) -> pd.Series:

    return df.apply(lambda x: x['source'] == x['target'], axis=1)

