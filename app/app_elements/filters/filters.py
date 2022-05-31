from .filter_funcs import *

FILTERS = [
    {
        'id': 'empty',
        'display_name': 'Empty',
        'mask': mask_empty,
        'scope_disabled': True
    },
    {
        'id': 'same',
        'display_name': 'Source = target',
        'mask': mask_same
    }
]