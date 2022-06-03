from flask import render_template, Blueprint, request

settings_ = Blueprint('settings_', __name__, template_folder='templates')

# ====================
@settings_.route('/settings', methods=['GET', 'POST'])
def settings():
    """Render source duplicate page"""

    if request.method == 'GET':
        return render_template('settings.html')