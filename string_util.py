def trim_string(s: str, limit: int = 128, postfix: str = ' ... (continues)'):
    """
    文字列を一定の長さ `limit` まで切り詰める\n
    一定以上の長さを持つ場合は長さの制限を超えないように前方を一部切り出して postfix を付加する
    """
    if len(s) <= limit:
        return s
    return s[:limit-len(postfix)] + postfix
