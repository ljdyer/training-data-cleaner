from flask import request, render_template, Blueprint, session
import json
from app_elements.filters.preview import generate_preview_df, get_next_n_rows, get_options, update_df
from app_elements.constants import PREVIEW_NUM_MAX

edit_ = Blueprint('edit_', __name__, template_folder='templates')

# ====================
@edit_.route('/edit', methods = ['GET', 'POST'])
def edit():
    """Render edit page"""

    if request.method == 'POST':
        json_data = request.get_json(force=True)
        action = json_data['action']

        if action == 'new_settings':
            settings = json_data['settings']
            generate_preview_df(settings)
            this_page, showing_from, showing_to, total = get_next_n_rows(PREVIEW_NUM_MAX)
            this_page['index'] = this_page.index
            options = get_options(settings)
            df_json = this_page.to_json(orient='records')
            return json.dumps({
                'df': df_json,
                'options': options,
                'showing_from': showing_from,
                'showing_to': showing_to,
                'showing_total': total
            })

        if action == 'next_page':
            this_page, showing_from, showing_to, total = get_next_n_rows(PREVIEW_NUM_MAX)
            this_page['index'] = this_page.index
            df_json = this_page.to_json(orient='records')
            return json.dumps({
                'df': df_json,
                'showing_from': showing_from,
                'showing_to': showing_to,
                'showing_total': total
            })

        if action == 'submit':
            remove = json_data['remove']
            update = json_data['update']
            update_df(remove, update)
            this_page, showing_from, showing_to, total = get_next_n_rows(PREVIEW_NUM_MAX)
            this_page['index'] = this_page.index
            df_json = this_page.to_json(orient='records')
            return json.dumps({
                'df': df_json,
                'showing_from': showing_from,
                'showing_to': showing_to,
                'showing_total': total
            })

        if action == 'start_over':
            generate_preview_df(session['current_settings'])
            this_page, showing_from, showing_to, total = get_next_n_rows(PREVIEW_NUM_MAX)
            this_page['index'] = this_page.index
            df_json = this_page.to_json(orient='records')
            return json.dumps({
                'df': df_json,
                'showing_from': showing_from,
                'showing_to': showing_to,
                'showing_total': total
            })


    if request.method == 'GET':
        return render_template('edit.html')