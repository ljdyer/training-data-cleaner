from typing import Callable

import pandas as pd
from app_elements.helper_functions.helper import (get_df, get_preview_df,
                                                  save_df, save_preview_df)
from flask import session

from ..filters import FILTERS
from ..orders import ORDERS
import html


# ====================
def escape_html(str_: str) -> str:

    escaped = html.escape(str(str_))
    return escaped


# ====================
def unescape_str(str_: str) -> str:

    return (str_
            .encode('latin1', 'backslashreplace')
            .decode('unicode-escape'))


# ====================
def generate_preview_df(settings: dict) -> pd.DataFrame:

    session['current_settings'] = settings
    if settings['mode'] == 'edit':
        return generate_preview_df_edit()
    elif settings['mode'] == 'find_replace':
        return generate_preview_df_find_replace()


# ====================
def generate_preview_df_edit() -> pd.DataFrame:

    settings = session['current_settings']
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
        other_col = 'target' if order_col == 'source' else 'source'
        preview_df = preview_df.sort_values(by=[order_col, other_col],
                                            ascending=ascending, key=key)

    session['start_index_next'] = 0
    save_preview_df(preview_df)
    return preview_df


# ====================
def generate_preview_df_find_replace() -> pd.DataFrame:

    df = get_df()
    settings = session['current_settings']
    search_re = settings['search_re']
    scope = settings['scope']
    mask = df['source'].str.contains(search_re, regex=True)
    if scope == 'source':
        mask = df['source'].str.contains(search_re, regex=True)
    elif scope == 'target':
        mask = df['target'].str.contains(search_re, regex=True)
    else:
        source_mask = df['source'].str.contains(search_re, regex=True)
        target_mask = df['target'].str.contains(search_re, regex=True)
        if scope == 'both':
            mask = pd.concat([source_mask, target_mask], axis=1).all(axis=1)
        elif scope == 'either':
            mask = pd.concat([source_mask, target_mask], axis=1).any(axis=1)
    preview_df = df[mask]
    session['start_index_next'] = 0
    save_preview_df(preview_df)
    return preview_df


# ====================
def get_next_n_rows(n: int):

    settings = session['current_settings']
    preview_df = get_preview_df()
    total = len(preview_df)
    if session['start_index_next'] >= total:
        preview_df = generate_preview_df(settings)
        total = len(preview_df)
    showing_from = session['start_index_next']
    showing_to = min(total - 1, showing_from + n - 1)
    session['start_index_next'] = session['start_index_next'] + n
    this_page = preview_df.iloc[showing_from:showing_to+1]
    this_page = this_page.applymap(escape_html)
    # Find/replace preview
    if settings['mode'] == 'find_replace':
        scope = settings['scope']
        search_re = settings['search_re']
        replace_re = settings['replace_re']
        regex = settings['regex']
        if scope != 'target':
            this_page['source'] = highlight_find_replace(this_page['source'],
                                                         search_re, replace_re,
                                                         regex)
        if scope != 'source':
            this_page['target'] = highlight_find_replace(this_page['target'],
                                                         search_re, replace_re,
                                                         regex)
    this_page['index'] = this_page.index
    return this_page, showing_from, showing_to, total


# ====================
def highlight_find_replace(col: pd.Series,
                           search_re: str,
                           replace_re: str,
                           regex: bool) -> pd.Series:

    if regex:
        # Increment all groups in replace regex (\1, \2, etc) by
        # 1 since \1 is used for preview.
        replace_re = increment_groups_by_1(replace_re)

    return col.str.replace(
        rf"({search_re})",
        rf"<del>\1</del><ins>{replace_re}</ins>",
        regex=True
    )


# ====================
def increment_groups_by_1(regex: str) -> str:

    if regex == '':
        return ''
    old = list(regex)
    new = []
    new.append(old.pop(0))
    while old:
        next = old.pop(0)
        if new[len(new) - 1] == '\\' and next.isnumeric():
            new.append(str(int(next) + 1))
        else:
            new.append(next)
    incremented = ''.join(new)
    print(incremented)
    return incremented


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
def apply_mask_func(df: pd.DataFrame,
                    mask_func: Callable,
                    filter_scope: str) -> pd.DataFrame:

    if filter_scope == 'source':
        mask = mask_func(df['source'])
    elif filter_scope == 'target':
        mask = mask_func(df['target'])
    elif filter_scope == 'both':
        mask = pd.concat([mask_func(df['source']), mask_func(df['target'])],
                         axis=1).all(axis=1)
    elif filter_scope == 'either':
        mask = pd.concat([mask_func(df['source']), mask_func(df['target'])],
                         axis=1).any(axis=1)

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


# ====================
def replace_all():

    df = get_df()
    settings = session['current_settings']
    assert settings['mode'] == 'find_replace'
    scope = settings['scope']
    search_re = settings['search_re']
    replace_re = settings['replace_re']
    regex = settings['regex']
    if scope != 'target':
        df['source'] = df['source'].str.replace(
            search_re, replace_re, regex=regex
        )
    if scope != 'source':
        df['target'] = df['target'].str.replace(
            search_re, replace_re, regex=regex
        )
    save_df(df)
