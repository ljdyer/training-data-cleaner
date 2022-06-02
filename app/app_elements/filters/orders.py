from .order_funcs import *

ORDERS = {
    'alphabetical': {
        'display_name': 'A-Z',
        'key': None
    },
    'length': {
        'display_name': 'Length',
        'key': sort_key_length
    },
    'ratio_source_target': {
        'display_name': 'Length of source relative to target',
        'key': sort_key_ratio,
        'whole_row': True
    }
}