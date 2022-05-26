"""
html_helper.py

Helper functions to generate HTML tables from pandas dataframes
"""

import pandas as pd
from .issues import ISSUES
from .diagnostics import keep


# ====================
def df_to_html_form(df: pd.DataFrame) -> str:
    """Generate an HTML form from a pandas dataframe"""

    form_html = (
        df.style
        .format({c: html_input(c) for c in df.columns}, na_rep='')
        .set_table_attributes('class="table table-packed"')
        .render()
    )
    return form_html


# ====================
def html_input(c):
    """Format a pandas cell as an HTML text input"""

    return ('<input class="form-control p-0 input-sm" name="{}" value="{{}}" />'
            .format(c))


# ====================
def df_to_html_table(df: pd.DataFrame, td_classes: pd.DataFrame = None) -> str:
    """Generate an HTML table from a pandas dataframe"""

    styler = (
        df.style
        .format(formatter=None, na_rep='')
        .set_table_attributes('class="table table-packed"')
    )
    if td_classes is not None:
        styler = styler.set_td_classes(td_classes)
    table_html = styler.render()
    return table_html


# ====================
def double_dup_preview(df: pd.DataFrame) -> str:
    """Generate a preview of double dupes in a pandas dataframe"""

    mask = ISSUES['double_dup']['mask_preview']
    all_double_dup_df = df[mask].sort_values([df.columns[0], df.columns[1]])
    td_classes = generate_first_instance_classes(all_double_dup_df)
    table_html = df_to_html_table(all_double_dup_df, td_classes)
    return table_html


# ====================
def generate_first_instance_classes(df: pd.DataFrame) -> pd.DataFrame:
    """Generate a dataframe of classes to indicate whether or not each row
    is a first instance"""

    def keep_or_remove_classes(is_dup: bool) -> str:
        # Green for first instance, red for subsequent instances
        return 'table-danger' if is_dup else 'table-success'

    is_first = df.duplicated(keep='first')
    classes = (pd.DataFrame([is_first, is_first])
               .transpose()
               .applymap(keep_or_remove_classes))
    classes.columns = df.columns
    return classes


# ====================
def source_dup_preview(df: pd.DataFrame) -> str:
    """Generate a preview of source dupes in a pandas dataframe"""

    mask = ISSUES['source_dup']['mask_preview']
    source_dup_df = keep(df, mask).sort_values([df.columns[0], df.columns[1]])
    td_classes = generate_group_classes(source_dup_df)
    table_html = df_to_html_table(source_dup_df, td_classes)
    return table_html


# ====================
def generate_group_classes(df: pd.DataFrame):
    """Generate a dataframe of classes to indicate groups of rows with
    the same value in the source column"""

    def group_classes(true_or_false: bool) -> str:
        return 'table-secondary' if true_or_false else 'table-dark'

    source_list = df[df.columns[0]].to_list()
    groups = [True]
    for idx in range(1, len(source_list)):
        if source_list[idx] == source_list[idx-1]:
            groups.append(groups[idx-1])
        else:
            groups.append(not groups[idx-1])
    groups = pd.Series(groups)
    classes = (pd.DataFrame([groups, groups])
               .transpose()
               .applymap(group_classes))
    classes.columns = df.columns
    classes.index = df.index
    return classes


# ====================
def empties_preview(df: pd.DataFrame) -> str:
    """Generate a preview of empties in a pandas dataframe"""

    def danger_if_empty(x: str) -> str:
        return 'table-danger' if x == '' else ''

    mask = ISSUES['empty']['mask']
    empties_df = keep(df, mask)
    td_classes = df.applymap(danger_if_empty)
    table_html = df_to_html_table(empties_df, td_classes)
    return table_html


# ====================
def sames_preview(df: pd.DataFrame) -> str:
    """Generate a preview of sames in a pandas dataframe"""

    mask = ISSUES['same']['mask']
    sames_df = keep(df, mask)
    table_html = df_to_html_table(sames_df)
    return table_html


# ====================
if __name__ == "__main__":

    pass
