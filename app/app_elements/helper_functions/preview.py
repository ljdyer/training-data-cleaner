from flask import session
import pandas as pd

from app_elements.helper_functions.helper import get_preview_df
from ..filters import FILTERS
from ..orders import ORDERS
from typing import Callable
from app_elements.helper_functions.helper import save_preview_df, get_df, save_df


# ====================
def generate_preview_df(settings: dict) -> pd.DataFrame:

    session['current_settings'] = settings
    df = get_df()
    # FILTER
    filter_id = settings['filter']
    filter = FILTERS[filter_id]
    mask_func = filter['mask']

    if filter.get('whole_row'):
        # Apply mask to whole df
        mask = mask_func(df)
        preview_df = df[mask]
    else:
        # Apply mask to selected column(s)
        filter_scope = settings['filter_scope']
        mask = apply_mask_func(df, mask_func, filter_scope)
        preview_df = df[mask]

    # SORT
    order_id = settings['order']
    order = ORDERS[order_id]
    # Ascending or descending?
    orientation = settings['order_orientation']
    ascending = bool(orientation == 'ascending')
    # Get key
    key = order['key']
    if order.get('whole_row'):
        # Sort based on whole row
        preview_df['sort_key'] = key(preview_df)
        preview_df = preview_df.sort_values(by='sort_key', ascending=ascending)
        preview_df = preview_df.drop(columns=['sort_key'])
    else:
        # Apply sort key to one column
        order_col = settings['order_col']
        other_col = 'target' if order_col=='source' else 'source'
        preview_df = preview_df.sort_values(by=[order_col, other_col], ascending=ascending, key=key)

    session['start_index_next'] = 0
    save_preview_df(preview_df)
    return preview_df


# ====================
def get_next_n_rows(n: int):

    preview_df = get_preview_df()
    total = len(preview_df)
    if session['start_index_next'] >= total:
        preview_df = generate_preview_df(session['current_settings'])
        total = len(preview_df)
    showing_from = session['start_index_next']
    showing_to = min(total - 1, showing_from + n - 1)
    session['start_index_next'] = session['start_index_next'] + n
    this_page = preview_df.iloc[showing_from:showing_to+1]
    this_page['index'] = this_page.index
    return this_page, showing_from, showing_to, total


# ====================
def get_options(settings: dict) -> dict:

    filter = FILTERS[settings['filter']]
    filter_whole_row = bool(filter.get('whole_row'))
    disable_remove_all = bool(filter.get('disable_remove_all'))
    order = ORDERS[settings['order']]
    order_whole_row = bool(order.get('whole_row'))
    options = {
        'filter_scope_disabled': filter_whole_row,
        'order_col_disabled': order_whole_row,
        'disable_remove_all': disable_remove_all
    }
    return options


# ====================
def apply_mask_func(df: pd.DataFrame, mask_func: Callable, filter_scope: str) -> pd.DataFrame:

    if filter_scope == 'source':
        mask = mask_func(df['source'])
    elif filter_scope == 'target':
        mask = mask_func(df['target'])
    elif filter_scope == 'both':
        mask = pd.concat([mask_func(df['source']), mask_func(df['target'])], axis=1).all(axis=1)
    elif filter_scope == 'either':
        mask = pd.concat([mask_func(df['source']), mask_func(df['target'])], axis=1).any(axis=1)

    return mask


# ====================
def update_df(rows_to_drop: list, rows_to_update: dict):

    df = get_df()

    # Remove rows
    df = df.drop(rows_to_drop, axis=0)

    # Update rows
    for index, content in rows_to_update.items():
        index = int(index)
        source, target = content
        assert index in df.index
        df.loc[index]['source'] = source
        df.loc[index]['target'] = target
    save_df(df)

    return len(df)


# ====================
def remove_all():

    preview_df = get_preview_df()
    rows_to_drop = preview_df.index.to_list()
    df = get_df()
    df = df.drop(rows_to_drop, axis=0)
    save_df(df)
    return len(df)
