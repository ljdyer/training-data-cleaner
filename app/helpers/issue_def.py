from .issue_functions import *

ISSUES = {
    'double_duplicate': {
        'singular': 'double duplicate',
        'plural': 'double duplicates',
        'recc_action': 'Remove all but the first instance of each',
        'mask': mask_double_dup,
        'mask_preview': mask_double_dup_preview,
        'preview': preview_double_dup,
        'remove_all': remove_all_double_dup
    },
    'empty': {
        'singular': 'empty',
        'plural': 'empties',
        'recc_action': 'Remove all',
        'mask': mask_empty,
        'mask_preview': mask_empty,
        'preview': preview_empty,
        'remove_all': remove_all_empty
    },
    'source_duplicate': {
        'singular': 'source duplicate',
        'plural': 'source duplicates',
        'recc_action': 'Select the best translation for each and remove the '
                       + 'rest',
        'mask': mask_source_dup,
        'mask_preview': mask_source_dup_preview
    },
    'same': {
        'singular': 'same',
        'plural': 'sames',
        'recc_action': 'Remove all',
        'mask': mask_same,
        'mask_preview': mask_same
    }
}