import os


separator = os.path.sep


def file_exists(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False
