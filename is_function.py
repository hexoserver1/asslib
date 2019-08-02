from types import FunctionType


def is_function(obj: object):
    return type(obj) is FunctionType
