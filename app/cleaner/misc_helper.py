"""
misc_helper.py

Miscellanous helper functions
"""

import datetime
import uuid

# ====================
def get_timestamp() -> str:
    """Get a timestamp of the current time suitable for appending
    to file names"""

    return datetime.datetime.now().strftime("%d%b%Y-%H%M%S")


# ====================
def get_random_secret_key() -> str:
    """Get a random secret key"""

    return uuid.uuid4().hex


# ====================
if __name__ == "__main__":

    print(uuid.uuid4().hex)