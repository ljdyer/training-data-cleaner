from flask import render_template, Blueprint

source_dup_ = Blueprint('source_dup_', __name__, template_folder='templates')

# ====================
@source_dup_.route('/source_dup')
def source_dup():
    """Render source duplicate page"""

    df = get_df()
    return render_template('source_dup.html')