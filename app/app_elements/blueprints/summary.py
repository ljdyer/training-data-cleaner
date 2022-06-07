from flask import render_template, Blueprint, url_for
from app_elements.helper_functions.helper import get_df
from app_elements.checks import CHECKS

summary_ = Blueprint('summary_', __name__, template_folder='templates')


# ====================
@summary_.route('/summary')
def summary():
    """Render summary page"""

    df = get_df()
    checks = []
    for check in CHECKS:
        result = check['func'](df)
        link = url_for(check['link_route'], **check['link_args'])
        checks.append({**check, **result, 'link': link})
    passed = [c for c in checks if c['status'] == 'pass']
    errors = [c for c in checks
              if c['status'] == 'fail'
              and c['type'] == 'error']
    warnings = [c for c in checks
                if c['status'] == 'fail'
                and c['type'] == 'warning']

    return render_template('summary.html',
                           passed=passed, errors=errors, warnings=warnings)
