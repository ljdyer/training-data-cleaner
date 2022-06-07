OPTIONS = {
    'PREVIEW_NUM_MAX': {
        'display': 'Number of rows to include on each page in Edit view.',
        'default': 100,
        'force_int': True,
        'type': 'INPUT'
    },
    'MAX_NUM_CHARS': {
        'display': """Number of characters to flag a cell as \'Too long\'.<br>
        <a href="https://cloud.google.com/translate/automl/docs/beginners-guide">Google AutoML docs</a> recommend 50 tokens (words).""",
        'default': 200,
        'force_int': True,
        'type': 'INPUT'
    }
}
