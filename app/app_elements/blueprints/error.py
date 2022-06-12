from flask import Blueprint, render_template, request, session

error_ = Blueprint('error_', __name__,
                   template_folder='templates')


# ====================
@error_.route('/error', methods=['GET'])
def error():
    """Render error page"""

    if request.method == 'GET':
        error_type = request.args.get('error_type')
        if error_type == 'more_than_one_file':
            print('session clear')
            session.clear()
        if error_type == 'df_read_error':
            print('session clear')
            session.clear()
        if error_type == 'not_xlsx':
            print('session clear')
            session.clear()
        return render_template('error.html', error_type=error_type)
