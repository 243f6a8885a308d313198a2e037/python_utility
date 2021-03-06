"""
from https://qiita.com/siroken3/items/4bb937fcfd4c2489d10a
"""

from functools import wraps


def on_timeout(limit, handler, hint=None):
    """
    指定した実行時間に終了しなかった場合、handlerをhint/limitを引数にして呼び出します
    @on_timeout(limit=3600, handler=notify_func, hint=u'長い計算')
    def long_time_function():
    """

    def notify_handler(signum, frame):
        handler("'%s' is not finished in %d second(s)." % (hint, limit))

    def __decorator(function):
        def __wrapper(*args, **kwargs):
            import signal
            signal.signal(signal.SIGALRM, notify_handler)
            signal.alarm(limit)
            try:
                result = function(*args, **kwargs)
            except Exception as e:
                signal.alarm(0)
                raise e
            signal.alarm(0)
            return result
        return wraps(function)(__wrapper)
    return __decorator
