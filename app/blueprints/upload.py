from flask import (redirect, render_template, request,
                   session, url_for)
import os
import pandas as pd
from cleaner.dataframe_helper import (read_df_from_excel)
from flask import Blueprint, current_app
from helpers.helper import save_df

upload_ = Blueprint('upload_', __name__, template_folder='templates')

# ====================
def get_upload_fpath(fname: str):

    return os.path.join(current_app.config['UPLOAD_FOLDER'], fname)


# ====================
def save_df(df: pd.DataFrame):

    session['df'] = df.to_dict()


@upload_.route('/')
def index():
    """Redirect to upload page on app start"""

    return redirect(url_for('upload_.upload_page'))



# ====================
@upload_.route('/upload_page')
def upload_page():
    """Render upload page"""

    return render_template('upload.html')


# ====================
@upload_.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload a file placed in dropzone"""

    print('upload')
    if request.method == 'POST':
        for f in request.files.getlist('file'):
            # There should only be one file due to limit placed on dropzone in
            # upload.html
            print('here')
            session['fpath'] = get_upload_fpath(f.filename)
            print('here')
            f.save(session['fpath'])
            # Store the filename
            session['fname'] = f.filename
            session['fname_root'], session['fname_ext'] = \
                os.path.splitext(session['fname'])

        # TODO: Validate file (type, num_columns, etc)
        df = read_df_from_excel(session['fpath'])
        save_df(df)
        session['source_column'] = df.columns[0]
        session['target_column'] = df.columns[1]

    print('running')
    return redirect(url_for('view_data'))