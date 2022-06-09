"""
checks.py

Defines checks that are carried out on training data in the 'summary' view.

The keys of the dictionary CHECKS are the IDs used to refer to the checks in
the app's code.

The items have the following keys:

'display': The display name used in the app's UI
'type': 'error' or 'warning'
'func': A function that takes a dataframe and returns the results of the check
        (see below for more details)
'link_route': A link to the route of the app where the user can rectify the
              issue
'link_args: The arguments to pass in the link the route specified in
            'link_route'

The function referenced in the 'func' key returns a dictionary object which
may contain the following keys:

'status' (REQUIRED): 'pass' or 'fail'
'message': A message to the user giving details about the status (if 'status'
           is 'fail')
"""

import pandas as pd
from app_elements.filters import (mask_empty, mask_same, mask_too_long)
from app_elements.helper_functions.helper import mask_source_dup
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
        long_cell_strings.append(f"<b>{long_target}</b> target " +
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


CHECKS = [
    {
        'id': 'source_dup',
        'display': 'Source duplicates',
        'type': 'error',
        'func': check_source_dup,
        'link_route': 'source_dup_.source_dup',
        'link_args': {}
    },
    {
        'id': 'empty',
        'display': 'Empties',
        'type': 'error',
        'func': check_empty,
        'link_route': 'edit_.edit',
        'link_args': {
            'filter': 'empty',
            'filter_scope': 'either',
            'order': 'index',
            'order_orientation': 'ascending'
        }
    },
    {
        'id': 'too_long',
        'display': 'Long cells',
        'type': 'warning',
        'func': check_too_long,
        'link_route': 'edit_.edit',
        'link_args': {
            'filter': 'too_long',
            'filter_scope': 'either',
            'order': 'length',
            'order_col': 'source',
            'order_orientation': 'descending'
        }
    },
    {
        'id': 'same',
        'display': 'Source = target',
        'type': 'warning',
        'func': check_same,
        'link_route': 'edit_.edit',
        'link_args': {
            'filter': 'same',
            'order': 'index',
            'order_orientation': 'ascending'
        }
    }
]
