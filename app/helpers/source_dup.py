# === SOURCE DUPLICATE ===

# ====================
def mask_source_dup(df: pd.DataFrame) -> pd.Series:

    return df.duplicated(subset=[df.columns[0]], keep='first')


# ====================
def mask_source_dup_preview(df: pd.DataFrame) -> pd.Series:

    return df.duplicated(subset=[df.columns[0]], keep=False)