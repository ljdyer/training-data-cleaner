"""
check_funcs.py
"""

import pandas as pd
from app_elements.helper_functions.source_dup import mask_source_dup
from app_elements.helper_functions.filter_funcs import mask_empty, mask_same, mask_too_long

PASS = {'status': 'pass'}


# ====================
def FAIL(message: str) -> dict:

    return {
        'status': 'fail',
        'message': message
    }


def s_if_plural(word: str, n: int) -> str:

    if n == 1:
        return word
    else:
        return word + 's'


# ====================
def check_source_dup(df: pd.DataFrame) -> dict:

    mask = mask_source_dup(df)
    source_dups = df[mask]
    num_duplicates = len(source_dups)
    if num_duplicates == 0:
        return PASS
    else:
        num_sources = len(source_dups['source'].unique())
        return FAIL(
            f"Your data contains {num_sources} source texts with more than one translation " +\
            f"({num_duplicates} duplicate rows)."
        )


# ====================
def check_empty(df: pd.DataFrame) -> dict:
    
    empty_source = mask_empty(df['source']).sum()
    empty_target = mask_empty(df['target']).sum()

    if empty_source > 0 and empty_target > 0:
        return FAIL(
            f"Your data contains {empty_source} empty source {s_if_plural('cell', empty_source)} " +\
            f"and {empty_target} empty target {s_if_plural('cell', empty_target)}."
        )
    elif empty_source > 0:
        return FAIL(
            f"Your data contains {empty_source} empty source {s_if_plural('cell', empty_source)}."
        )
    elif empty_target > 0:
        return FAIL(
            f"Your data contains {empty_target} empty target {s_if_plural('cell', empty_target)}."
        )
    else:
        return PASS


# ====================
def check_too_long(df: pd.DataFrame) -> dict:
    
    


# ====================
def check_same(df: pd.DataFrame) -> dict:
    pass