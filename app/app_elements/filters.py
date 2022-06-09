from flask import current_app
import pandas as pd


# ====================
def mask_none(df: pd.DataFrame) -> pd.Series:

    return df.apply(lambda x: True, axis=1)


# ====================
def mask_empty(col: pd.Series) -> pd.Series:

    return col.apply(lambda x: x == '')


# ====================
def mask_same(df: pd.DataFrame) -> pd.Series:

    return df.apply(lambda x: x['source'] == x['target'], axis=1)


# ====================
def mask_too_long(col: pd.Series) -> pd.Series:

    return col.apply(lambda x: len(x) > current_app.config['MAX_NUM_CHARS'])


# ====================
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
