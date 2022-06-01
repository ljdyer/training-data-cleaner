from .order_funcs import *

ORDERS = {
    'length': {
        'display_name': 'Length',
        'key': sort_key_length
    },
    'ratio_source_target': {
        'display_name': 'Ratio of lengths (source:target)',
        'key': sort_key_ratio,
        'whole_row': True
    }

}