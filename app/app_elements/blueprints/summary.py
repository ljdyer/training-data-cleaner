from flask import render_template, Blueprint

summary_ = Blueprint('summary_', __name__, template_folder='templates')

# ====================
@summary_.route('/summary')
def summary():
    """Render summary page"""

    # df = get_df()
    # passed, failed, remaining = diagnose_issues(df, FILTERS, ISSUE_NAMES)
    return render_template('summary.html')
    # , passed=passed, failed=failed, remaining=remaining)