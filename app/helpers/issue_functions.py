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

ACTIONS = [
    ACTION_SELECT_ALL,
    ACTION_DESELECT_ALL,
    ACTION_SKIP,
    ACTION_SUBMIT,
    ACTION_REMOVE_ALL_DUPLICATES
]


# === DOUBLE DUPLICATE ===

# ====================
def mask_double_dup(df: pd.DataFrame) -> pd.Series:

    return df.duplicated(keep='first')


# ====================
def mask_double_dup_preview(df: pd.DataFrame) -> pd.Series:

    return df.duplicated(keep=False)


# ====================
def preview_double_dup(df: pd.DataFrame) -> pd.DataFrame:

    preview_df = df[mask_double_dup_preview(df)].sort_values(['source', 'target']).head(100)
    preview_df['keep'] = ~mask_double_dup(preview_df)
    action_remove_all_dups = ACTION_REMOVE_ALL_DUPLICATES.copy()
    num_in_dataset = len(df[mask_double_dup])
    action_remove_all_dups['text'] = f'Remove all {num_in_dataset} duplicates in data'
    action_remove_all_dups['class'] = 'btn-success'
    actions = [action_remove_all_dups]
    
    return preview_df, actions


# ====================
def remove_all_double_dup(df: pd.DataFrame) -> pd.DataFrame:

    df = remove(df, mask_double_dup)
    return df



# === EMPTY ===

# ====================
def mask_empty(df: pd.DataFrame) -> pd.Series:

    return df.applymap(lambda x: x == '').any(axis=1)


# ====================
def preview_empty(df: pd.DataFrame) -> pd.DataFrame:

    preview_df = df[mask_empty(df)].sort_values(['source', 'target'])
    return preview_df


# === SOURCE DUPLICATE ===

# ====================
def mask_source_dup(df: pd.DataFrame) -> pd.Series:

    return df.duplicated(subset=[df.columns[0]], keep='first')


# ====================
def mask_source_dup_preview(df: pd.DataFrame) -> pd.Series:

    return df.duplicated(subset=[df.columns[0]], keep=False)


# ====================
def mask_same(df: pd.DataFrame) -> pd.Series:

    source_col = df.columns[0]
    target_col = df.columns[1]
    return df.apply(lambda x: x[source_col] == x[target_col], axis=1)


