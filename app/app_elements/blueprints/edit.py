from flask import request, render_template, Blueprint
import json
from app_elements.filters.filters import FILTERS
from app_elements.filters.preview import preview
from helpers.helper import get_df, keep, save_df

edit_ = Blueprint('edit_', __name__, template_folder='templates')

# ====================
@edit_.route('/edit', methods = ['GET', 'POST'])
def edit():
    """Render edit page"""
    df = get_df()

    if request.method == 'POST':
        print(request)
        print(request.args)
        filter = request.args.get('filter')
        print(filter)
        filter_scope = request.args.get('filter_scope')
        order = request.args.get('order')
        order_col = request.args.get('order_col')
        order_orientation = request.args.get('order_orientation')
        # USE df.to_json()

        df = preview(df, filter, filter_scope, order, order_col, order_orientation)
        return json.dumps({'success': 'true'})

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