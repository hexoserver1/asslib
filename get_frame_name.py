import inspect


def get_frame_name(stack=None, context=1, literal=False):
    stack = inspect.stack(context=context) if stack is None else stack
    level = 0 if literal else 1
    return stack[level][3]
