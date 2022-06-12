import datetime
import os

import pandas as pd
from app_elements.helper_functions.helper import get_df
from flask import Blueprint, current_app, send_from_directory, session

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


# ====================
def escape_for_excel(content_str: str) -> str:
    """Prepare dataframe cell content for writing to Excel"""

    # Escape strings beginning with '=' so that Excel does not interpret them
    # as formulas
    if content_str.startswith('='):
        return f"'{content_str}"
    # If there are no issues, return the original string
    else:
        return content_str


# ====================
def write_excel(df: pd.DataFrame, path: str):
    """Write pandas dataframe to Excel file"""

    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    sheet_name = 'training_data'
    df = df.fillna('').applymap(escape_for_excel)
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    worksheet = writer.sheets[sheet_name]
    worksheet.set_column(0, 1, 50)  # First and second columns
    writer.save()


# ====================
def generate_download_fname():

    return f"{session['fname_root']}_{get_timestamp()}.{session['fname_ext']}"


# ====================
def get_download_fpath(fname):

    return os.path.join(current_app.config['DOWNLOAD_FOLDER'], fname)


# ====================
def get_timestamp() -> str:
    """Get a timestamp of the current time suitable for appending
    to file names"""

    return datetime.datetime.now().strftime("%d%b%Y-%H%M%S")
