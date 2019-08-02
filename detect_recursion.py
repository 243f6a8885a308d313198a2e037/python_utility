# https://stackoverflow.com/questions/36662181/is-there-a-way-to-check-if-function-is-recursive-in-python

import bdb
import sys


class RecursionDetected(Exception):
    pass


class RecursionDetector(bdb.Bdb):
    def do_clear(self, arg):
        pass

    def __init__(self, *args):
        bdb.Bdb.__init__(self, *args)
        self.stack = set()

    def user_call(self, frame, argument_list):
        code = frame.f_code
        if code in self.stack:
            raise RecursionDetected
        self.stack.add(code)

    def user_return(self, frame, return_value):
        self.stack.remove(frame.f_code)


def test_recursion(func):
    detector = RecursionDetector()
    detector.set_trace()
    try:
        func()
    except RecursionDetected:
        return True
    else:
        return False
    finally:
        sys.settrace(None)
