from .helper_functions.filter_funcs import (mask_empty, mask_none, mask_same,
                                            mask_too_long)

FILTERS = {
    'none': {
        'display_name': '(None)',
        'mask': mask_none,
        'whole_row': True,
        'disable_remove_all': True
    },
    'empty': {
        'display_name': 'Empty',
        'mask': mask_empty
    },
    'same': {
        'display_name': 'Source = target',
        'mask': mask_same,
        'whole_row': True
    },
    'too_long': {
        'display_name': 'Too long',
        'mask': mask_too_long,
    }
}
