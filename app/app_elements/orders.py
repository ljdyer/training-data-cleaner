import pandas as pd


# ====================
def sort_key_length(col: pd.Series) -> pd.Series:

    return col.str.len()


# ====================
def sort_key_ratio(df: pd.DataFrame) -> pd.Series:

    len_source = df['source'].str.len()
    len_target = df['target'].str.len()
    # Smoothing to avoid zero division
    len_target = len_target.apply(lambda x: 0.01 if x == 0 else x)
    ratio = len_source.div(len_target)
    return ratio


# ====================
def sort_key_index(df: pd.DataFrame) -> pd.Series:

    return df.index


# ====================
def sort_key_percent_alpha(col: pd.Series) -> pd.Series:

    len_all = col.str.len()
    alpha_only = col.str.replace(r'[^a-zA-Z]', '', regex=True)
    len_alpha = alpha_only.str.len()
    len_all = len_all.apply(lambda x: 0.01 if x == 0 else x)
    percent_alpha = len_alpha.div(len_all)
    print(percent_alpha)
    return(percent_alpha)


# ====================
ORDERS = {
    'index': {
        'display_name': 'Order in data file',
        'key': sort_key_index,
        'whole_row': True
    },
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
    },
    'percent_alpha': {
        'display_name': 'Percentage of alphabetic letters (a-z or A-Z)',
        'key': sort_key_percent_alpha
    }
}
