from app_elements.helper_functions.download_helper import write_excel
from app_elements.helper_functions.helper import (generate_download_fname,
                                                  get_df, get_download_fpath)
from flask import Blueprint, current_app, send_from_directory

download_ = Blueprint('download_', __name__, template_folder='templates')


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
