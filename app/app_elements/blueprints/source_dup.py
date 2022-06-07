import json

from app_elements.helper_functions.helper import check_df_in_session
from app_elements.helper_functions.preview import update_df
from app_elements.helper_functions.source_dup_helper import (
    generate_source_dups, get_next_source_dup)
from flask import Blueprint, render_template, request

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
            remove = json_data['remove']
            update = json_data['update']
            print(remove)
            df_len = update_df(remove, update)
            response['df_len'] = df_len

        this_page, source_num, num_sources = get_next_source_dup()
        df_json = this_page.to_json(orient='records')
        response = {**response, 'df': df_json, 'source_num': source_num,
                    'num_sources': num_sources}
        return json.dumps(response)

    if request.method == 'GET':
        check_df_in_session()
        return render_template('source_dup.html')
