# ====================
def pluralize(number, singular='', plural='s'):
    """Template filter to pluralize strings depending on their number"""

    return singular if number == 1 else plural


# ====================
def more_than_zero(number, zero, more_than_zero):

    return zero if number == 0 else more_than_zero


# ====================
def title_case(str_):

    return str_.title()


# ====================
def snake_case(str_):

    return '_'.join(str_.split(''))