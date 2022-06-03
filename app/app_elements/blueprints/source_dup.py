from flask import render_template, Blueprint, request
from app_elements.helper_functions.source_dup import generate_source_dups, get_next_source_dup
from app_elements.helper_functions.preview import update_df
from app_elements.helper_functions.helper import get_df
import json

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
            print(update)
            df_len = update_df(remove, update)
            response['df_len'] = df_len
            
        this_page, source_num, num_sources = get_next_source_dup()
        df_json = this_page.to_json(orient='records')
        response = {**response, 'df': df_json, 'source_num': source_num, 'num_sources': num_sources}
        return json.dumps(response)

    if request.method == 'GET':
        # Call get_df to trigger error if no data has been uploaded
        df = get_df()
        return render_template('source_dup.html')