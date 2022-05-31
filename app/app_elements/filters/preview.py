import pandas as pd
from .filters import FILTERS

def preview(df: pd.DataFrame,
            filter: str,
            filter_scope: str,
            order: str,
            order_column: str,
            order_orientation: str) -> pd.DataFrame:

    print(filter)
    mask = FILTERS[filter]['mask']
    preview_df = df[mask(df)]
    return preview_df