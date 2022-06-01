import pandas as pd
from .filters import FILTERS
from .orders import ORDERS

def preview(df: pd.DataFrame, settings: dict) -> pd.DataFrame:

    # FILTER
    filter_id = settings['filter']
    filter = FILTERS[filter_id]
    mask_func = filter['mask']
    if filter.get('whole_row'):
        # Apply mask to whole df
        mask = mask_func(df)
        preview_df = df[mask]
    else:
        filter_scope = settings['filter_scope']
        if filter_scope == 'source':
            mask = mask_func(df['source'])
        elif filter_scope == 'target':
            mask = mask_func(df['target'])
        elif filter_scope == 'both':
            mask = pd.concat([mask_func(df['source']), mask_func(df['target'])], axis=1).all(axis=1)
        elif filter_scope == 'either':
            mask = pd.concat([mask_func(df['source']), mask_func(df['target'])], axis=1).any(axis=1)
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
        # Apply sort_func to whole df
        preview_df['sort_key'] = key(preview_df)
        preview_df.sort_values(by=['sort_key'], ascending=ascending, key=key)
        preview_df = preview_df.drop(columns=['sort_key'])
    else:
        # Apply sort key to one column
        order_col = settings['order_col']
        print(order_col, ascending)
        other_col = 'target' if order_col=='source' else 'source'
        preview_df = preview_df.sort_values(by=[order_col, other_col], ascending=ascending, key=key)

    return preview_df.head(100)