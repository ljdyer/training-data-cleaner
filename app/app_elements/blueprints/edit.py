from flask import request, render_template, Blueprint
import json
from helpers.filters.filters import FILTERS
from helpers.helper import get_df, keep, save_df

edit_ = Blueprint('edit_', __name__, template_folder='templates')

# ====================
@edit_.route('/edit', methods = ['GET', 'POST'])
def edit():
    """Render edit page"""
    df = get_df()

    if request.method == 'POST':
        filter_id = request.values.get('filter_id')
        action = request.values.get('action')
        if action == 'remove_all':
            df = FILTERS[filter_id]['remove_all'](df)
            save_df(df)
            return json.dumps({'success': True})

    if request.method == 'GET':
        filter_id = request.args.get('filter_id')
        action = request.args.get('action')
        # Generate preview
        if filter_id is None:
            return render_template('edit.html')
        else:
            mask = FILTERS[filter_id]['mask']
            preview_df = keep(df, mask).sort_values(['source', 'target'])
            return render_template('edit.html', filter_id=filter_id, df=preview_df)