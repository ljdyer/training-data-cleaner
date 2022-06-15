import json
from operator import itemgetter

from app_elements.helper_functions.helper import check_df_in_session
from app_elements.helper_functions.preview_helper import (generate_preview_df,
                                                          get_next_n_rows,
                                                          get_options,
                                                          remove_all,
                                                          remove_rows,
                                                          update_rows)
from flask import Blueprint, current_app, render_template, request, session

edit_ = Blueprint('edit_', __name__, template_folder='templates')


# ====================
@edit_.route('/edit', methods=['GET', 'POST'])
def edit():
    """Render edit page"""

    if request.method == 'POST':
        json_data = request.get_json(force=True)
        action = json_data['action']
        response = {}
        if action == 'new_settings':
            settings = json_data['settings']
            print(settings)
            settings['mode'] = 'edit'
            generate_preview_df(settings)
            response['options'] = get_options(settings)
        elif action == 'view_index':
            settings = {
                'filter': 'none',
                'filter_scope': 'source',
                'order': 'index',
                'order_col': 'source',
                'order_orientation': 'ascending'
            }
            index = json_data['index']
            generate_preview_df(settings, index)
            pass
        elif action == 'next_page':
            pass
        elif action == 'submit':
            remove, update = itemgetter('remove', 'update')(json_data)
            update_rows(update)
            df_len = remove_rows(remove)
            response['df_len'] = df_len
        elif action == 'start_over':
            generate_preview_df(session['current_settings'])
        elif action == 'remove_all':
            df_len = remove_all()
            response['df_len'] = df_len
            generate_preview_df(session['current_settings'])
        this_page, showing_from, showing_to, total = get_next_n_rows(
            current_app.config['PREVIEW_NUM_MAX']
        )
        df_json = this_page.to_json(orient='records')
        response = {
            **response, 'df': df_json, 'showing_from': showing_from,
            'showing_to': showing_to, 'showing_total': total
        }
        return json.dumps(response)

    if request.method == 'GET':
        check_df_in_session()
        if request.args.get('filter'):
            return render_template(
                'edit.html',
                filter=request.args.get('filter'),
                filter_scope=request.args.get('filter_scope'),
                order=request.args.get('order'),
                order_col=request.args.get('order_col'),
                order_orientation=request.args.get('order_orientation')
            )
        else:
            return render_template(
                'edit.html',
                filter='none',
                filter_scope=None,
                order='index',
                order_col=None,
                order_orientation='ascending'
            )
