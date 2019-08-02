import os
import shutil


def fetch_data_files(*files):
    for f in files:
        shutil.copyfile(os.path.join('data', f), f)


def read_data_files_as_string(*files, encoding='utf-8'):
    data = []
    for f in files:
        with open(f, encoding=encoding) as ff:
            data.append(ff.read())
    return data


def clear_data_files(*files):
    for f in files:
        os.remove(f)
