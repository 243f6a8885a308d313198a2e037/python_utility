def filter_source(source, get_import=True, get_funcdef=True):
    """
    ソースコードを一部条件に従って抜き出す
    """
    result = []
    for line in source.split('\n'):
        if line == '':
            result.append(line)
        elif line[0:7] == 'import ':
            if get_import:
                result.append(line)
        elif line[0:5] == 'from ':
            if get_import:
                result.append(line)
        elif line[0:4] == 'def ' or line[0:6] == 'class ' or line[0] == ' ' or line[0] == '\t':
            if get_funcdef:
                result.append(line)
    return '\n'.join(result)
