from flask import request, render_template, Blueprint, session, current_app
import json
from app_elements.helper_functions.preview import generate_find_df, get_next_n_rows
from app_elements.helper_functions.helper import get_df

find_replace_ = Blueprint('find_replace_', __name__, template_folder='templates')


# ====================
@find_replace_.route('/find_replace', methods=['GET', 'POST'])
def find_replace():
    """Render find_replace page"""

    if request.method == 'POST':
        json_data = request.get_json(force=True)
        action = json_data['action']
        print(action)
        response = {}
        if action == 'search':
            search_re = json_data['search_re']
            generate_find_df(search_re)
        this_page, showing_from, showing_to, total = get_next_n_rows(
            current_app.config['PREVIEW_NUM_MAX']
        )
        df_json = this_page.to_json(orient='records')
        response = {**response, 'df': df_json, 'showing_from': showing_from,
                    'showing_to': showing_to, 'showing_total': total}
        return json.dumps(response)

    if request.method == 'GET':
        # Call get_df to trigger error if no data has been uploaded
        df = get_df()
        return render_template('find_replace.html')
