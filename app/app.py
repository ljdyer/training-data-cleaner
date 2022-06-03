"""
app.py

Main program for training data cleaner
"""

import os

import pandas as pd
import redis
from flask import Flask, render_template
from flask_dropzone import Dropzone
from flask_session import Session

from app_elements.blueprints.download import download_
from app_elements.blueprints.edit import edit_
from app_elements.blueprints.source_dup import source_dup_
from app_elements.blueprints.settings import settings_
from app_elements.blueprints.summary import summary_
from app_elements.blueprints.upload import upload_
from app_elements.blueprints.view_data import view_data_
from app_elements.context_processor import provide_context_info
from app_elements.exceptions import NoDataException
from app_elements.options import OPTIONS
from app_elements.template_filters import more_than_zero, pluralize, title_case

pd.options.mode.chained_assignment = None  # default='warn'

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
# Set default options
for option_id, option in OPTIONS.items():
    app.config[option_id] = option['default']

# Routes
app.register_blueprint(upload_)
app.register_blueprint(edit_)
app.register_blueprint(summary_)
app.register_blueprint(download_)
app.register_blueprint(settings_)
app.register_blueprint(source_dup_)
app.register_blueprint(view_data_)
# Template filters
app.jinja_env.filters['more_than_zero'] = more_than_zero
app.jinja_env.filters['pluralize'] = pluralize
app.jinja_env.filters['title_case'] = title_case
# Context processor
app.context_processor(provide_context_info)

dropzone = Dropzone(app)

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
    return render_template('upload.html', error_type='not_xlsx')


# ====================
if __name__ == "__main__":

    app.run(debug=True)
