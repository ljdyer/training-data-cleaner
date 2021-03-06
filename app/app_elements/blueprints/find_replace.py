import json
import re
from operator import itemgetter

from app_elements.helper_functions.helper import check_df_in_session
from app_elements.helper_functions.preview_helper import (generate_preview_df,
                                                          get_next_n_rows,
                                                          remove_all,
                                                          remove_rows,
                                                          replace_all,
                                                          update_rows)
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
            if not settings['regex']:
                settings['search_re'] = re.escape(settings['search_re'])
            generate_preview_df(settings)
        elif action == 'next_page':
            pass
        elif action == 'replace_all':
            replace_all()
        elif action == 'replace_remove':
            remove, update = itemgetter('remove', 'update')(json_data)
            df_len = remove_rows(remove)
            update_rows(update)
            response['df_len'] = df_len
        elif action == 'replace_leave':
            update = json_data['update']
            update_rows(update)
        elif action == 'remove_all':
            df_len = remove_all()
            response['df_len'] = df_len
            generate_preview_df(session['current_settings'])
        (this_page_marked, this_page_unmarked, showing_from, showing_to,
         total) = \
            get_next_n_rows(current_app.config['PREVIEW_NUM_MAX'])
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
        if request.args.get('find'):
            return render_template(
                'find_replace.html',
                find=request.args.get('find'),
                scope=request.args.get('scope'),
                use_regex=request.args.get('use_regex'),
                replace=request.args.get('replace')
            )
        else:
            return render_template(
                'find_replace.html',
                find='',
                scope='source',
                use_regex=False,
                replace=''
            )
