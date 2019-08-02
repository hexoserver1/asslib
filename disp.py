def disp(*args, do_print=True):
    """
        disp(msg)

        where
            msg is a string to print

        Prints a string prepended with caller information

        title - disp vr - 1.2 author - fakas date - 20190225

        mods - 1.1 Added current time to output (thogar20190514)
               1.2 Changes to avoid warnings and better conform to Python conventions (fakas20190708)

        """
    import time
    import traceback

    now = time.strftime('%d/%m/%y-%X')
    # noinspection PyBroadException
    try:  # Just in case...
        import inspect

        frame = inspect.stack()
        if type(frame) is list:
            frame = frame[1]

        file = frame[1].split('/')[-1]
        line = str(frame[2])
        func = frame[3]

        caller = '.'.join((func, file)) + " (" + line + ")"

        args = list(args)  # Because tuples are immutable
        args[0] = now + " " + caller + ": " + args[0]  # Prepend caller info
    except Exception:
        traceback.print_exc()

    if do_print:
        print(*args)

    return args
