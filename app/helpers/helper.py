import pandas as pd
from flask import session

# ====================
def save_df(df: pd.DataFrame):

    session['df'] = df.to_dict()
