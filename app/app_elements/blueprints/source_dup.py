import json
from typing import Tuple

from operator import itemgetter
import pandas as pd
from app_elements.helper_functions.helper import (check_df_in_session, get_df,
                                                  mask_source_dup)
from app_elements.helper_functions.preview import update_rows, remove_rows
from flask import Blueprint, render_template, request, session

source_dup_ = Blueprint('source_dup_', __name__, template_folder='templates')


# ====================
@source_dup_.route('/source_dup', methods=['GET', 'POST'])
def source_dup():
    """Render source duplicate page"""

    if request.method == 'POST':
        json_data = request.get_json(force=True)
        action = json_data['action']
        response = {}

        if action == 'start_over':
            generate_source_dups()
        elif action == 'next_page':
            pass
        elif action == 'submit':
            remove, update = itemgetter('remove', 'update')(json_data)
            update_rows(update)
            df_len = remove_rows(remove)
            response['df_len'] = df_len

        this_page, source_num, num_sources = get_next_source_dup()
        df_json = this_page.to_json(orient='records')
        response = {**response, 'df': df_json, 'source_num': source_num,
                    'num_sources': num_sources}
        return json.dumps(response)

    if request.method == 'GET':
        check_df_in_session()
        return render_template('source_dup.html')


# ====================
def generate_source_dups() -> list:
    """Generate the list of source duplicates

    Return a list of unique source strings"""

    df = get_df()
    duplicated = df[mask_source_dup]
    source_dups = duplicated['source'].unique()
    session['start_source_next'] = 0
    session['source_dups'] = source_dups
    return source_dups


# ====================
def get_next_source_dup() -> Tuple[pd.DataFrame, int, int]:
    """Get the next source duplicate

    Return a 3-tuple containing the following elements:
    - The next set of source, target pairs to display (type: pd.DataFrame)
    - The number (index) of this source duplicate
    - The total number of unique sources
    """

    df = get_df()
    source_dups = session['source_dups']
    num_sources = len(source_dups)
    if session['start_source_next'] >= num_sources:
        source_dups = generate_source_dups()
        num_sources = len(source_dups)
        if num_sources == 0:
            return pd.DataFrame(), 0, 0
    source_num = session['start_source_next']
    this_source = source_dups[source_num]
    this_source_dup = df[df['source'] == this_source]
    session['start_source_next'] += 1
    this_source_dup['index'] = this_source_dup.index
    return this_source_dup, source_num, num_sources
