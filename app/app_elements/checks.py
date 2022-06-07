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

The function referenced in the 'func' key returns a dictionary object which
may contain the following keys:

'status' (REQUIRED): 'pass' or 'fail'
'message': A message to the user giving details about the status (if 'fail')
'link': A link to the part of the app where the user can rectify the issue
"""

from app_elements.helper_functions.check_funcs import (check_empty, check_same,
                                                       check_source_dup,
                                                       check_too_long)

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
            'filter_scope': 'either'
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
        }
    }
]
