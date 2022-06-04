"""
check_funcs.py
"""

import pandas as pd
from flask import current_app
from app_elements.helper_functions.source_dup import mask_source_dup
from app_elements.helper_functions.filter_funcs import mask_empty, mask_same, mask_too_long

PASS = {'status': 'pass'}


# ====================
def FAIL(message: str) -> dict:

    return {
        'status': 'fail',
        'message': message
    }


# ====================
def s_if_plural(word: str, n: int) -> str:

    if n == 1:
        return word
    else:
        return word + 's'


# ====================
def is_or_are(n: int) -> str:

    if n == 1:
        return 'is'
    elif n > 1:
        return 'are'


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
    
    long_source = mask_too_long(df['source']).sum()
    long_target = mask_too_long(df['target']).sum()

    if long_source > 0 and long_target > 0:
        return FAIL(
            f"Your data contains {long_source} source {s_if_plural('cell', long_source)} " +\
            f"and {long_target} target {s_if_plural('cell', long_target)} that are " +\
            f"more than {current_app.config['MAX_NUM_CHARS']} long.<br>" +\
            "The Google AutoML docs recommend that you \"split items into individual sentences " +\
            "where possible\"."
        )
    elif long_source > 0:
        return FAIL(
            f"Your data contains {long_source} source {s_if_plural('cell', long_source)} " +\
            f"that {is_or_are(long_source)} more than {current_app.config['MAX_NUM_CHARS']} long.<br>" +\
            "The Google AutoML docs recommend that you \"split items into individual sentences " +\
            "where possible\"."
        )
    elif long_target > 0:
        return FAIL(
            f"Your data contains {long_target} target {s_if_plural('cell', long_target)} " +\
            f"that {is_or_are(long_target)} more than {current_app.config['MAX_NUM_CHARS']} long.<br>" +\
            "The Google AutoML docs recommend that you \"split items into individual sentences " +\
            "where possible\"."
        )
    else:
        return PASS


# ====================
def check_same(df: pd.DataFrame) -> dict:
    pass