import inspect
from os import path


def get_frame(stack=None, context=1, level=1):
    stack = inspect.stack(context=context) if stack is None else stack
    return stack[level]


def get_function_name(stack=None, context=1, level=1):
    level += 1
    frame = get_frame(stack=stack, context=context, level=level)
    return frame.function


def get_file_name(stack=None, context=1, level=1):
    level += 1
    frame = get_frame(stack=stack, context=context, level=level)
    return frame.filename


def get_directory(stack=None, context=1, level=1):
    level += 1
    file_name = get_file_name(stack=stack, context=context, level=level)
    return path.dirname(file_name)


def get_class_file(obj):
    if type(obj) is not type:
        obj = obj.__class__
    return inspect.getfile(obj)
