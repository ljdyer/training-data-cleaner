from app_elements.helper_functions.helper import get_df
from flask import render_template, Blueprint, current_app

view_data_ = Blueprint('view_data_', __name__, template_folder='templates')


# ====================
@view_data_.route('/view_data')
def view_data():

    df = get_df()
    num_rows = min(current_app.config['PREVIEW_SAMPLE'], len(df))
    preview_df = df.sample(num_rows)
    preview_df['index'] = preview_df.index
    return render_template('view_data.html', df=preview_df)
