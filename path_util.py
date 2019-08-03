import os

def assure_directory_existence(dir_path: str):
    """ ディレクトリの存在を保証する """
    if os.path.isdir(dir_path):
        return
    if os.path.exists(dir_path):
        raise FileExistsError(dir_path)
    os.mkdir(dir_path)

def assure_file_existence(file_path: str, encoding: str, *, default_content: str = None):
    """ ファイルの存在を保証する """
    if os.path.isfile(file_path):
        return
    if os.path.exists(file_path):
        raise FileExistsError(file_path)
    if default_content is not None:
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(default_content)
