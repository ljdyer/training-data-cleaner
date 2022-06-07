"""
check_funcs.py
"""

import pandas as pd
from app_elements.helper_functions.filter_funcs import (mask_empty, mask_same,
                                                        mask_too_long)
from app_elements.helper_functions.source_dup import mask_source_dup
from flask import current_app

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
            f"Your data contains <b>{num_sources}</b> source texts with " +
            f"more than one translation (<b>{num_duplicates}</b> duplicate " +
            "rows)."
        )


# ====================
def check_empty(df: pd.DataFrame) -> dict:

    empty_source = mask_empty(df['source']).sum()
    empty_target = mask_empty(df['target']).sum()
    empty_cell_strings = []
    if empty_source > 0:
        empty_cell_strings.append(f"<b>{empty_source}</b> empty source " +
                                  s_if_plural('cell', empty_source))
    if empty_target > 0:
        empty_cell_strings.append(f"<b>{empty_target}</b> empty target " +
                                  s_if_plural('cell', empty_target))
    if empty_cell_strings:
        return FAIL(
            f"Your data contains {' and '.join(empty_cell_strings)}."
        )
    else:
        return PASS


# ====================
def check_too_long(df: pd.DataFrame) -> dict:

    long_source = mask_too_long(df['source']).sum()
    long_target = mask_too_long(df['target']).sum()
    long_cell_strings = []
    if long_source > 0:
        long_cell_strings.append(f"<b>{long_source}</b> source " +
                                 s_if_plural('cell', long_source))
    if long_target > 0:
        long_cell_strings.append(f"<b>{long_target}</b> source " +
                                 s_if_plural('cell', long_target))
    if long_source > 0 and long_target > 0:
        return FAIL(
            f"Your data contains {' and '.join(long_cell_strings)} that are " +
            f"more than {current_app.config['MAX_NUM_CHARS']} characters long."
        )
    else:
        return PASS


# ====================
def check_same(df: pd.DataFrame) -> dict:

    mask = mask_same(df)
    sames = df[mask]
    num_sames = len(sames)
    if num_sames == 0:
        return PASS
    else:
        return FAIL(
            f"Your data contains <b>{num_sames}</b> rows where the source " +
            "is the same as the target."
        )
