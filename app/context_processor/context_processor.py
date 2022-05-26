from flask import session
from cleaner.issues import ISSUES
import pandas as pd

def provide_context_info():
    """Context processer to provide data info to Jinja templates"""

    issues_and_pages = [(issue_id, issue_info['link_text'])
                        for issue_id, issue_info in ISSUES.items()]

    context = {'issues_and_pages': issues_and_pages}
    try:
        df = pd.DataFrame(session['df'])
        data_info = {'fname': session['fname'],
                     'num_rows': len(df)}
        context = {**context, **data_info}
    except KeyError:
        pass

    return context