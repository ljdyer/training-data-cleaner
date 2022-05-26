"""
excel_helper.py

Helper functions for writing dataframes to Excel files
"""

import pandas as pd


# ====================
def escape_for_excel(content_str: str) -> str:
    """Prepare dataframe cell content for writing to Excel"""

    # Escape strings beginning with '=' so that Excel does not interpret them
    # as formulas
    if content_str.startswith('='):
        return f"'{content_str}"
    # If there are no issues, return the original string
    else:
        return content_str


# ====================
def write_excel(df: pd.DataFrame, path: str):
    """Write pandas dataframe to Excel file"""

    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    sheet_name = 'training_data'
    df = df.fillna('').applymap(escape_for_excel)
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    worksheet = writer.sheets[sheet_name]
    worksheet.set_column(0, 1, 50)  # First and second columns
    writer.save()
