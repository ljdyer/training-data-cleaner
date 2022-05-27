import pandas as pd
# from cleaner.issues import ISSUES
from constants.constants import *
from flask import session


# ====================
def provide_context_info():
    """Context processer to provide data info to Jinja templates"""

    context = {'pages': PAGES, 'issues': ISSUE_NAMES}
    try:
        df = pd.DataFrame(session['df'])
        data_info = {'fname': session['fname'],
                     'num_rows': len(df)}
        context = {**context, **data_info}
    except KeyError:
        pass

    return context
