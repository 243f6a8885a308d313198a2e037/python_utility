def filter_source(source, *, get_if=True, get_with=True, get_import=True, get_funcdef=True, comment_out_prefix='## >> '):
    """
    ソースコードを一部条件に従って抜き出す
    """

    lines = []
    for line in source.split('\n'):
        is_kept = None
        if line == '' or line[0] == '#':
            is_kept = True
        elif line.startswith('if '):
            is_kept = get_if
        elif line.startswith('with '):
            is_kept = get_with
        elif line.startswith('import ') or line.startswith('from '):
            is_kept = get_import
        elif line.startswith('def ') or line.startswith('class ') or line[0] in ' \t':
            is_kept = get_funcdef
        else:
            is_kept = False

        lines.append(('' if is_kept else comment_out_prefix) + line)

    return '\n'.join(lines)
