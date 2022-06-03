from flask import render_template, Blueprint, request, current_app
from app_elements.options import OPTIONS

settings_ = Blueprint('settings_', __name__, template_folder='templates')

# ====================
@settings_.route('/settings', methods=['GET', 'POST'])
def settings():
    """Render source duplicate page"""

    if request.method == "POST":
        new_vals = request.form
        for option, new_val in new_vals.items():
            if OPTIONS[option]['force_int']:
                current_app.config[option] = int(new_val)
        options = OPTIONS.copy()
        for option in options.keys():
            options[option]['current'] = current_app.config[option]
        return render_template('settings.html', options=options)

    if request.method == 'GET':
        if request.args.get('action') == 'restore_defaults':
            options = get_default_options()
        else:
            options = get_current_options()
        return render_template('settings.html', options=options)


# ====================
def get_current_options():

    options = OPTIONS.copy()
    for option in options.keys():
        options[option]['current'] = current_app.config[option]
    return options


# ====================
def get_default_options():

    options = OPTIONS.copy()
    for option in options.keys():
        options[option]['current'] = options[option]['default']
    return options

