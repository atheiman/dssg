import os


def get_abs_path(path):
    path.rstrip('/')
    if not path.startswith('/'):
        path = os.path.join(os.getcwd(), path)
    return path
