import os

import pandas as pd
import json
from flask import (Blueprint, current_app, redirect, render_template, request,
                   session, url_for)
from helpers.helper import save_df, read_and_preprocess

upload_ = Blueprint('upload_', __name__, template_folder='templates')

# ====================
@upload_.route('/')
def index():
    """Redirect to upload page on app start"""

    return redirect(url_for('upload_.upload'))


# ====================
@upload_.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload a file placed in dropzone"""

    if request.method == 'POST':
        # Save file
        files = request.files.getlist('file')
        # There should only be one file
        if len(files) > 1:
            # TODO: Handle error
            assert False
        file = files[0]
        fname = file.filename
        fpath = get_upload_fpath(fname)
        file.save(fpath)
        save_fname_info_to_session(fname)
        # TODO: Validate file (type, num_columns, etc)
        df, num_removed = read_and_preprocess(fpath)
        num_remaining = len(df)
        session['num_removed'] = num_removed
        session['num_remaining'] = num_remaining
        save_df(df)
        return json.dumps({'success': True})

    else:
        if request.args.get('file_uploaded'):
            return render_template('upload.html', file_uploaded=True)
        return render_template('upload.html')


# ====================
def get_upload_fpath(fname: str):

    return os.path.join(current_app.config['UPLOAD_FOLDER'], fname)


# ====================
def save_df(df: pd.DataFrame):

    session['df'] = df.to_dict()


# ====================
def save_fname_info_to_session(fname: str):

    session['fname'] = fname
    session['fname_root'], session['fname_ext'] = \
        os.path.splitext(fname)