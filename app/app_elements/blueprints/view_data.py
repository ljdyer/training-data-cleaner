from helpers.helper import get_df
from flask import render_template, Blueprint

view_data_ = Blueprint('view_data_', __name__, template_folder='templates')

# ====================
@view_data_.route('/view_data')
def view_data():

    df = get_df()
    df['index'] = df.index
    return render_template('view_data.html', df=df)