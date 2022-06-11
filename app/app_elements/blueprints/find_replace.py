import json
import re

from app_elements.helper_functions.helper import check_df_in_session
from app_elements.helper_functions.preview import (generate_preview_df,
                                                   get_next_n_rows, remove_all,
                                                   replace_all)
from flask import Blueprint, current_app, render_template, request, session

find_replace_ = Blueprint('find_replace_', __name__,
                          template_folder='templates')


# ====================
@find_replace_.route('/find_replace', methods=['GET', 'POST'])
def find_replace():
    """Render find_replace page"""

    if request.method == 'POST':
        json_data = request.get_json(force=True)
        action = json_data['action']
        print(action)
        response = {}
        if action == 'preview':
            settings = json_data['settings']
            settings['mode'] = 'find_replace'
            print(settings['regex'])
            print(settings['search_re'])
            if not settings['regex']:
                settings['search_re'] = re.escape(settings['search_re'])
            print(settings['search_re'])
            generate_preview_df(settings)
        elif action == 'next_page':
            pass
        elif action == 'submit':
            pass
        elif action == 'start_over':
            pass
        elif action == 'replace_all':
            replace_all()
        elif action == 'remove_all':
            df_len = remove_all()
            response['df_len'] = df_len
            generate_preview_df(session['current_settings'])
        this_page_marked, this_page_unmarked, showing_from, showing_to, total = get_next_n_rows(
            current_app.config['PREVIEW_NUM_MAX']
        )
        df_json = this_page_marked.to_json(orient='records')
        df_json_unmarked = this_page_unmarked.to_json(orient='records')
        response = {
            **response,
            'df': df_json,
            'df_unmarked': df_json_unmarked,
            'showing_from': showing_from,
            'showing_to': showing_to,
            'showing_total': total
        }
        return json.dumps(response)

    if request.method == 'GET':
        check_df_in_session()
        return render_template('find_replace.html')
