import os
import re
import json


def find_all_code_cells_matched(filename, codetag):
    with open(filename) as f:
        # NOTE 拡張子が .ipynb でも信じてはいけない (.html を打ちなおしたっぽい人がいた)
        try:
            j = json.load(f)
        except Exception:
            print(f"warning: file {filename} cannot be parsed as json.")
            return
        # NOTE Jupyter Notebook の人と Colaboratory の人で json の構造が異なる
        cells = None
        if 'cells' in j:
            cells = j['cells']
        elif 'worksheets' in j:
            if 'cells' in j['worksheets'][0]:
                cells = j['worksheets'][0]['cells']
        if cells is None:
            print(f"warning: given Jupyter Notebook {filename} has no 'cells' property.")
            return
        for cell in cells:
            if 'cell_type' not in cell:
                print(cell)
                print("warning: given Jupyter Notebook cell has no 'cell_type' property.")
                continue
            if cell['cell_type'] != "code":
                continue
            source_list = None
            if 'source' in cell:
                source_list = cell['source']
            elif 'input' in cell:
                source_list = cell['input']
            if source_list is None:
                print(cell)
                print("warning: given Jupyter Notebook cell has no 'source' or 'input' property.")
                continue
            source = ''.join(source_list)
            if re.search(codetag, source, re.MULTILINE):
                yield source

def jpynb_cell_quarrier(codetag):
    def func(files):
        possibles = []
        for file in files:
            for possible in find_all_code_cells_matched(file, codetag):
                possibles.append(possible)
        if len(possibles) == 0:
            return None
        elif len(possibles) == 1:
            return possibles[0][1]
        else:
            for index, cell in enumerate(possibles):
                print("---- cell [ {} ]; codetag: [ {} ]; filename: [ {} ] ----"
                      .format(index, codetag, os.path.basename(cell[0])))
                print(cell[1])
            print("--------------------------------------------------------------")
            print("Which cell is appropriate to evaluate? [0-{}]".format(len(possibles) - 1))
            while True:
                cellidx = input("> cell ")
                # cellidx = len(possibles) - 1
                # cellidx = 0
                try:
                    cellidx = int(cellidx)
                    if cellidx == -1:
                        return None
                    if 0 <= cellidx and cellidx < len(possibles):
                        return possibles[cellidx][1]
                except Exception:
                    pass
                print("[ {} ] is out of range. Please input appropriate index.".format(cellidx))
    return func


def jpynb_source_quarrier_with_cache(cached, codetag):
    def func(dirname):
        files_all = sorted(os.listdir(dirname))
        if cached in files_all:
            try:
                return open(os.path.join(dirname, cached)).read()
            except UnicodeDecodeError as e:
                return "raise Exception(\"UnicodeDecodeError: {}\")".format(str(e))
        files = [f for f in files_all if ".ipynb" in f and os.path.isfile(os.path.join(dirname, f))]
        files = [os.path.join(dirname, f) for f in files]
        return jpynb_cell_quarrier(codetag)(files)
    return func
