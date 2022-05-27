from typing import Callable, Tuple

import pandas as pd


# ====================
def get_diagnostic_results(df: pd.DataFrame) -> dict: 

    results = ISSUES.copy()
    new_df = df.copy()

    for issue in ISSUES.keys():
        results[issue]['num'] = get_num(df, ISSUES[issue]['mask'])
        new_df = remove(new_df, ISSUES[issue]['mask'])
        results[issue]['remaining'] = len(new_df)

    return results