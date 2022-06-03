from flask import render_template, Blueprint
from app_elements.helper_functions.helper import get_df

summary_ = Blueprint('summary_', __name__, template_folder='templates')

# ====================
@summary_.route('/summary')
def summary():
    """Render summary page"""

    # df = get_df()
    # passed, failed, remaining = diagnose_issues(df, FILTERS, ISSUE_NAMES)
    df = get_df()
    return render_template('summary.html')
    # , passed=passed, failed=failed, remaining=remaining)