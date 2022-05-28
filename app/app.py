"""
app.py

Main program for training data cleaner
"""

import os

import pandas as pd
import redis
from flask import Flask, render_template, request, send_from_directory, session
from flask_dropzone import Dropzone
from flask_session import Session

from app_elements.blueprints.upload import upload_
from app_elements.context_processor import *
from app_elements.template_filters import *
from app_elements.constants import *
from helpers.excel import *
from helpers.helper import *

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

# Routes
app.register_blueprint(upload_)
# Template filters
app.jinja_env.filters['more_than_zero'] = more_than_zero
app.jinja_env.filters['pluralize'] = pluralize
app.jinja_env.filters['title_case'] = title_case
# Context processor
app.context_processor(provide_context_info)

dropzone = Dropzone(app)


# ====================
@app.route('/edit', methods = ['GET'])
def edit():
    """Render edit page"""

    issue_id = request.args.get('issue_id')
    action = request.args.get('action')

    if issue_id is None:
        preview_df = pd.DataFrame()

    else:
        df = get_df()
        if action == 'remove_all':
            mask = ISSUES[issue_id]['mask']
            df = remove(df, mask)
            save_df(df)

        # Generate preview
        if issue_id == 'double_duplicate':
            preview_df = ISSUES['double_duplicate']['preview'](df)
        else:
            mask = ISSUES[issue_id]['mask_preview']
            preview_df = keep(df, mask).sort_values(['source', 'target'])

    return render_template('edit.html', issue_id=issue_id, df=preview_df)


# ====================
@app.route('/summary')
def summary():
    """Render edit page"""

    df = get_df()
    passed, failed, remaining = diagnose_issues(df, ISSUES, ISSUE_NAMES)
    return render_template('summary.html', passed=passed, failed=failed, remaining=remaining)


# ====================
@app.route('/download')
def download():
    """Download current version of training data file"""

    df = get_df()
    print(session['fname_root'])
    download_fname = generate_download_fname()
    print(download_fname)
    download_fpath = get_download_fpath(download_fname)
    print(df)
    write_excel(df, download_fpath)

    return send_from_directory(
        directory=app.config['DOWNLOAD_FOLDER'],
        path="", filename=download_fname
    )


# ====================
@app.route('/view_data')
def view_data():

    df = get_df()
    columns = df.columns
    # data_html = df_to_html_table(df)
    print('yo')
    return render_template('view_data.html', columns=columns, df=df)


# === ERROR HANDLERS ===


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
