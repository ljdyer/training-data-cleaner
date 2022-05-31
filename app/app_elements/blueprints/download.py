from flask import current_app, render_template, Blueprint, send_from_directory

download_ = Blueprint('download_', __name__, template_folder='templates')

from helpers.excel import write_excel
from helpers.helper import get_df, generate_download_fname, get_download_fpath

# ====================
@download_.route('/download')
def download():
    """Download current version of training data file"""

    df = get_df()
    download_fname = generate_download_fname()
    download_fpath = get_download_fpath(download_fname)
    write_excel(df, download_fpath)

    return send_from_directory(
        directory=current_app.config['DOWNLOAD_FOLDER'],
        path="", filename=download_fname
    )
