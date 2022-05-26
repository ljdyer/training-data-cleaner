from .masks import *

ISSUES = {
    'empty': {
        'singular': 'empty',
        'plural': 'empties',
        'recc_action': 'Remove all',
        'mask': mask_empty,
        'link_text': 'Empties'
    },
    'double_dup': {
        'singular': 'double duplicate',
        'plural': 'double duplicates',
        'recc_action': 'Remove all but the first instance of each',
        'mask': mask_double_dup,
        'mask_preview': mask_double_dup_preview,
        'link_text': 'Double duplicates'
    },
    'source_dup': {
        'singular': 'source duplicate',
        'plural': 'source duplicates',
        'recc_action': 'Select the best translation for each and remove the '
                       + 'rest',
        'mask': mask_source_dup,
        'mask_preview': mask_source_dup_preview,
        'link_text': 'Source duplicates'
    },
    'same': {
        'singular': 'same',
        'plural': 'sames',
        'recc_action': 'Remove all',
        'mask': mask_same,
        'link_text': 'Sames'
    }
}