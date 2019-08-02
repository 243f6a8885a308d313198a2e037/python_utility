import sys
import math


# 下位4bitは許す
def compare_float32(lhs, rhs, epsilon=2**-19):
    if lhs == rhs:
        return True
    diff = abs(lhs - rhs)
    if 0 in (lhs, rhs, diff):
        return (diff < sys.float_info.min)
    return diff / min(abs(lhs), abs(rhs)) < epsilon


# 下位8bitは許す
def compare_float64(lhs, rhs, epsilon=2**-44):
    if lhs == rhs:
        return True
    diff = abs(lhs - rhs)
    if 0 in (lhs, rhs, diff):
        return (diff < sys.float_info.min)
    return (diff / min(abs(lhs), abs(rhs))) < epsilon


COMPRES_PRECISELY_EQUAL = "PreciselyEqual"
COMPRES_ROUGHLY_EQUAL = "RoughlyEqual"
COMPRES_ROUGHLY_NOT_EQUAL = "RoughlyNotEqual"
COMPRES_PRECISELY_NOT_EQUAL = "PreciselyNotEqual"
COMPRES_DIFFERENT_TYPES = "DifferentTypes"
COMPRES_NON_SUPPORTED_TYPE = "NonSupportedType"
COMPRES = (
    COMPRES_PRECISELY_EQUAL, COMPRES_ROUGHLY_EQUAL, COMPRES_ROUGHLY_NOT_EQUAL,
    COMPRES_PRECISELY_NOT_EQUAL, COMPRES_DIFFERENT_TYPES, COMPRES_NON_SUPPORTED_TYPE)


# いろいろなデータ構造の場合に対応
# 対応構造: list, tuple, dict, float, int, str, type
def compare_with_float(lhs, rhs):
    if type(lhs) != type(rhs):
        return COMPRES.index(COMPRES_DIFFERENT_TYPES)
    if type(lhs) == float:
        if lhs == rhs:
            return COMPRES.index(COMPRES_PRECISELY_EQUAL)
        return COMPRES.index(COMPRES_ROUGHLY_EQUAL if compare_float64(lhs, rhs) else COMPRES_ROUGHLY_NOT_EQUAL)
    if type(lhs) in (int, str, type):
        return COMPRES.index(COMPRES_PRECISELY_EQUAL if lhs == rhs else COMPRES_PRECISELY_NOT_EQUAL)
    if type(lhs) in (tuple, list):
        code_summary = COMPRES.index(COMPRES_PRECISELY_EQUAL)
        for l, r in zip(lhs, rhs):
            code = compare_with_float(l, r)
            code_summary = max(code_summary, code)
        return code_summary
    if type(lhs) == dict:
        if len(lhs) != len(rhs):
            return COMPRES.index(COMPRES_PRECISELY_NOT_EQUAL)
        code_summary = COMPRES.index(COMPRES_PRECISELY_EQUAL)
        for key in lhs:
            code = compare_with_float(lhs[key], rhs[key])
            code_summary = max(code_summary, code)
        return code_summary
    if hasattr(lhs, '__eq__'):
        return COMPRES.index(COMPRES_PRECISELY_EQUAL if lhs == rhs else COMPRES_PRECISELY_NOT_EQUAL)
    print("compare_with_float: type", type(lhs), "is not supported")
    sys.exit(1)
    return COMPRES.index(COMPRES_NON_SUPPORTED_TYPE)


# 精確に等しいか
def is_precisely_equal(code):
    return code == COMPRES.index(COMPRES_PRECISELY_EQUAL)


# 大まかに等しいか
def is_roughly_equal(code):
    return code <= COMPRES.index(COMPRES_ROUGHLY_EQUAL)


# find value from value list, precisely and ambiguously
# MEMO 同一値は values にはないものとする
# MEMO 類似値は最も先頭にあるものを返す
def find_with_compare_with_float(value, values):
    roughly_equal = None
    for v in values:
        code = compare_with_float(value, v)
        if is_precisely_equal(code):
            return v
        if is_roughly_equal(code):
            roughly_equal = roughly_equal if roughly_equal else v
    return roughly_equal
