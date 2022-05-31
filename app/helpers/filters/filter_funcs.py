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
def mask_empty(df: pd.DataFrame) -> pd.Series:

    return df.applymap(lambda x: x == '').any(axis=1)


# ====================
def get_rows(df: pd.DataFrame, mask: Callable):

    return df[mask_empty(df)]




# ====================
def preview_empty(df: pd.DataFrame) -> pd.DataFrame:

    preview_df = df[mask_empty(df)].sort_values(['source', 'target'])
    if preview_df.empty:
        return None, None
    preview_df['keep'] = False
    action_remove_all = ACTION_REMOVE_ALL_DUPLICATES.copy()
    action_remove_all['text'] = f'Remove all {len(preview_df)} empties in data'
    action_remove_all['class'] = 'btn-success'
    actions = [ACTION_SELECT_ALL, ACTION_DESELECT_ALL, ACTION_SKIP, ACTION_SUBMIT, action_remove_all]

    return preview_df, actions


# ====================
def remove_all_empty(df: pd.DataFrame) -> pd.DataFrame:

    df = remove(df, mask_empty)
    return df


# ====================
def mask_same(df: pd.DataFrame) -> pd.Series:

    source_col = df.columns[0]
    target_col = df.columns[1]
    return df.apply(lambda x: x[source_col] == x[target_col], axis=1)


