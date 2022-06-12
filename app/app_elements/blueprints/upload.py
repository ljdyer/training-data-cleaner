import json
import werkzeug
import os
import pandas as pd

from typing import Tuple

from flask import current_app
from app_elements.helper_functions.helper import save_df
from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)

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
        file = request.files.getlist('file')[0]
        fname = file.filename
        fname_root, fname_ext = os.path.splitext(fname)
        fpath = get_upload_fpath(fname)
        file.save(fpath)
        if fname_ext != '.xlsx':
            return json.dumps({'success': False, 'error': 'not_xlsx'})
        try:
            df, num_removed = read_and_preprocess(fpath)
        except:
            return json.dumps({'success': False, 'error': 'df_read_error'})
        num_remaining = len(df)
        save_info_to_session({'fname': fname, 'fname_root': fname_root,
                              'fname_ext': fname_ext,
                              'num_removed': num_removed,
                              'num_remaining': num_remaining})
        save_df(df)
        return json.dumps({'success': True})

    else:
        if request.args.get('file_uploaded'):
            return render_template('upload.html', file_uploaded=True)
        return render_template('upload.html')


# ====================
def read_and_preprocess(fpath: str) -> Tuple[pd.DataFrame, int]:
    """Read a dataframe from an Excel file and perform preliminary cleaning
    operations"""

    df = pd.read_excel(fpath, engine="openpyxl")
    # Fill NaN with empty strings
    df = df.fillna('')
    # Strip leading/trailing spaces
    df = df.applymap(lambda x: x.strip())
    # Rename source and target columns
    df.columns = ['source', 'target']
    # Remove source+target duplicates
    new_df, num_removed = remove_double_duplicates(df)

    return new_df, num_removed


# ====================
def remove_double_duplicates(df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:

    dd_mask = df.duplicated(keep='first')
    num_removed = dd_mask.sum()
    new_df = df[~dd_mask]
    return new_df, num_removed


# ====================
def get_upload_fpath(fname: str):

    return os.path.join(current_app.config['UPLOAD_FOLDER'], fname)


# ====================
def save_info_to_session(info: dict):

    for key, value in info.items():
        session[key] = value


# ====================
def get_file(files: list) -> werkzeug.datastructures.FileStorage:
    """Get a unique file from a list of files"""

    # Raise exception if there is more than one file
    # if len(files) > 1:
    #     raise MoreThanOneFileException
    # Return the first (and only) file
    return files[0]
