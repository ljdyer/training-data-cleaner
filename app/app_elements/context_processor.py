import pandas as pd
# from cleaner.issues import FILTERS
from app_elements.constants import *
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

    try:
        upload_info = {
            'num_removed': session['num_removed'],
            'num_remaining': session['num_remaining']
        }
        context = {**context, **upload_info}
    except KeyError:
        pass

    print(context)

    return context
