"""
app.py

Main program for training data cleaner
"""

import os
from typing import Callable

import pandas as pd
import redis
from flask import (Flask, json, redirect, render_template, request,
                   send_from_directory, session, url_for)
from flask_dropzone import Dropzone
from flask_session import Session

from context_processor.context_processor import provide_context_info
from cleaner.dataframe_helper import (get_first_dup_df, get_source_dup_df,
                                      read_df_from_excel)
from cleaner.diagnostics import (get_diagnostic_results, get_num_and_remaining,
                                 remove)
from cleaner.excel_helper import write_excel
from cleaner.html_helper import (df_to_html_table, double_dup_preview,
                                 empties_preview, sames_preview,
                                 source_dup_preview)
from cleaner.issues import ISSUES
from cleaner.misc_helper import get_timestamp

from helpers.helper import save_df

from blueprints.upload import upload_

basedir = os.path.abspath(os.path.dirname(__file__))

# Configure redis and secret key
is_prod = os.environ.get('IS_HEROKU', None)
if is_prod:
    redis_host = os.environ.get('REDIS_HOST')
    redis_port = os.environ.get('REDIS_PORT')
    redis_password = os.environ.get('REDIS_PASSWORD')
    session_redis = redis.Redis(host=redis_host, port=redis_port, password=redis_password)
    secret_key = os.environ.get('SECRET_KEY')
else:
    # Local environment
    redis_url = 'redis://localhost:6379'
    session_redis = redis.from_url(redis_url)
    secret_key = 'bananas'

# Configure app
app = Flask(__name__)
app.config.update(
    SECRET_KEY=secret_key,
    UPLOAD_FOLDER=os.path.join(basedir, 'uploads'),
    DOWNLOAD_FOLDER=os.path.join(basedir, 'downloads'),
    SESSION_TYPE='redis',
    SESSION_PERMANENT=False,
    SESSION_USE_SIGNER=True,
    SESSION_REDIS=session_redis
)
server_session = Session(app)

app.register_blueprint(upload_)
app.context_processor(provide_context_info)

dropzone = Dropzone(app)

MAIN_PAGES = [
    ('upload_page', 'Upload file'),
    ('overview', 'Overview'),
    ('view_data', 'View data')
]


# === GENERAL FUNCTIONS ===

# ====================
def get_df() -> pd.DataFrame:

    try:
        return pd.DataFrame(session['df'])
    except Exception as e:
        raise NoDataException


# ====================
def generate_download_fname():

    f"{session['fname_root']}_{get_timestamp()}.{session['fname_ext']}"


# ====================
def get_download_fpath(fname):

    os.path.join(app.config['DOWNLOAD_FOLDER'], fname)


# ====================
def generate_preview(issue_id: str, preview: Callable):

    df = get_df()
    num, remaining = get_num_and_remaining(df, ISSUES[issue_id]['mask'])
    data_html = None
    if num > 0:
        data_html = preview(df)
    return num, remaining, data_html


# ====================
def remove_and_save(issue_id: str):
    df = get_df()
    df = remove(df, ISSUES[issue_id]['mask'])
    save_df(df)


# ====================
def get_skipped_sources():

    if 'skipped_sources' not in session:
        skipped_sources = []
    else:
        skipped_sources = session['skipped_sources']
    return skipped_sources


# ====================
def add_skipped_source(source_text):

    skipped_sources = get_skipped_sources()
    session['skipped_sources'] = skipped_sources + [source_text]


# ====================
def reset_skipped_sources():

    session['skipped_sources'] = []


# ====================
def drop_rows(rows_to_remove):

    df = get_df()
    df = df.drop(rows_to_remove)
    save_df(df)


# === TEMPLATE FILTERS ===


# ====================
@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    """Template filter to pluralize strings depending on their number"""

    return singular if number == 1 else plural


# ====================
@app.template_filter('more_than_zero')
def more_than_zero(number, zero, more_than_zero):
    """Template filter to pluralize strings depending on their number"""

    return zero if number == 0 else more_than_zero


# === CONTEXT PROCESSORS ===




# === ROUTES ===







# ====================
@app.route('/edit/<string:issue_id>', methods=['GET'])
def edit(issue_id):
    """Render edit page"""

    return render_template('edit.html', issue_id=issue_id)


# ====================
@app.route('/download')
def download():
    """Download current version of training data file"""

    df = get_df()
    download_fname = generate_download_fname()
    download_fpath = get_download_fpath(download_fname)
    write_excel(df, download_fpath)

    return send_from_directory(
        directory=app.config['DOWNLOAD_FOLDER'],
        path="", filename=download_fname
    )


# ====================
@app.route('/overview')
def overview():

    reset_skipped_sources()
    df = get_df()
    results = get_diagnostic_results(df)
    return render_template('overview.html', results=results)


# ====================
@app.route('/view_data')
def view_data():

    df = get_df()
    data_html = df_to_html_table(df)
    print('yo')
    return render_template('view_data.html', data_html=data_html)


# === ERROR HANDLERS ===


# ====================
class NoDataException(Exception):
    pass


# ====================
class NotXlsxException(Exception):
    pass


# ====================
@app.errorhandler(500)
def error500(error):
    return render_template('error.html', error_type='500', error_msg=error)


# ====================
@app.errorhandler(NoDataException)
def handle_no_data_exception(e):
    return render_template('error.html', error_type='no_df')


# ====================
@app.errorhandler(NotXlsxException)
def handle_not_xlsx_exception(e):
    print('raised')
    return render_template('upload.html', error_type='not_xlsx')


# ====================
if __name__ == "__main__":

    app.run(debug=True)
