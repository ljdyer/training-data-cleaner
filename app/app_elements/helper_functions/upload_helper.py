import os
from flask import current_app, session


# ====================
def get_upload_fpath(fname: str):

    return os.path.join(current_app.config['UPLOAD_FOLDER'], fname)


# ====================
def save_fname_info_to_session(fname: str):

    session['fname'] = fname
    session['fname_root'], session['fname_ext'] = \
        os.path.splitext(fname)
