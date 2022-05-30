from .issue_functions import *

ISSUES = {
    'empty': {
        'singular': 'empty',
        'plural': 'empties',
        'recc_action': 'Remove all',
        'mask': mask_empty,
    },
    'same': {
        'singular': 'same',
        'plural': 'sames',
        'recc_action': 'Remove all',
        'mask': mask_same,
    }
}