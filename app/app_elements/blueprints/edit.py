from flask import request, render_template, Blueprint, session, current_app
import json
from app_elements.helper_functions.preview import generate_preview_df, get_next_n_rows, get_options, update_df, remove_all
from app_elements.helper_functions.helper import get_df

edit_ = Blueprint('edit_', __name__, template_folder='templates')

# ====================
@edit_.route('/edit', methods = ['GET', 'POST'])
def edit():
    """Render edit page"""

    if request.method == 'POST':
        json_data = request.get_json(force=True)
        action = json_data['action']
        response = {}

        if action == 'new_settings':
            settings = json_data['settings']
            generate_preview_df(settings)
            response['options'] = get_options(settings)
        elif action == 'next_page':
            pass
        elif action == 'submit':
            remove = json_data['remove']
            update = json_data['update']
            df_len = update_df(remove, update)
            response['df_len'] = df_len
        elif action == 'start_over':
            generate_preview_df(session['current_settings'])
        elif action == 'remove_all':
            df_len = remove_all()
            response['df_len'] = df_len
            generate_preview_df(session['current_settings'])
            
        this_page, showing_from, showing_to, total = get_next_n_rows(current_app.config['PREVIEW_NUM_MAX'])
        df_json = this_page.to_json(orient='records')
        response = {**response, 'df': df_json, 'showing_from': showing_from, 'showing_to': showing_to, 'showing_total': total}
        return json.dumps(response)

    if request.method == 'GET':
        # Call get_df to trigger error if no data has been uploaded
        df = get_df()
        return render_template('edit.html')