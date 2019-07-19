class Collection:
    """
    Object to facilitate attribute invocation
    """
    def __init__(self, **args):
        self.__dict__.update(args)
