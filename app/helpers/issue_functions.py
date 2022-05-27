"""
issue_functions.py
"""

import pandas as pd


# === DOUBLE DUPLICATE ===

# ====================
def mask_double_dup(df: pd.DataFrame) -> pd.Series:

    return df.duplicated(keep='first')


# ====================
def mask_double_dup_preview(df: pd.DataFrame) -> pd.Series:

    return df.duplicated(keep=False)


# ====================
def preview_double_dup(df: pd.DataFrame) -> pd.DataFrame:

    preview_df = df[mask_double_dup_preview(df)].sort_values(['source', 'target'])
    preview_df['keep'] = ~mask_double_dup(preview_df)
    return preview_df


# === EMPTY ===

# ====================
def mask_empty(df: pd.DataFrame) -> pd.Series:

    return df.applymap(lambda x: x == '').any(axis=1)


# ====================
def preview_empty(df: pd.DataFrame) -> pd.DataFrame:

    preview_df = df[mask_empty(df)].sort_values(['source', 'target'])
    return preview_df


# === SOURCE DUPLICATE ===

# ====================
def mask_source_dup(df: pd.DataFrame) -> pd.Series:

    return df.duplicated(subset=[df.columns[0]], keep='first')


# ====================
def mask_source_dup_preview(df: pd.DataFrame) -> pd.Series:

    return df.duplicated(subset=[df.columns[0]], keep=False)


# ====================
def mask_same(df: pd.DataFrame) -> pd.Series:

    source_col = df.columns[0]
    target_col = df.columns[1]
    return df.apply(lambda x: x[source_col] == x[target_col], axis=1)
