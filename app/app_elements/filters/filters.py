from .filter_funcs import *

FILTERS = {
    'none': {
        'display_name': '(None)',
        'mask': mask_none
    },
    'empty': {
        'display_name': 'Empty',
        'mask': mask_empty
    },
    'same': {        
        'display_name': 'Source = target',
        'mask': mask_same,
        'whole_row': True
    }
}