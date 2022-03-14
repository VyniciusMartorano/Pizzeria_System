import shutil
import os


def copy_file_to_new_path(file_to_copy_path: str, path_target: str, new_name_file: str):
    new_path = f'{path_target}/{new_name_file}.db'
    
    if not os.path.exists(path_target):
        shutil.copy(file_to_copy_path, path_target)
        