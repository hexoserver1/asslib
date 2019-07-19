def str2num(strin):
    """
        Function used to execute commands in the terminal. Prints any errors to logs
        :param strin: A numeric string or list of the same
        :return num: is the converted result

        Changelog:
        Updates to better conform to Python conventions (fakas20190708)

        """

    pack = False
    t2l = False
    nan = float('NaN')
    if type(strin) is tuple:
        t2l = True
        strin = list(strin)
    elif type(strin) is not list:
        pack = True
        strin = [strin]
    for ii, vv in enumerate(strin):
        try:
            if vv.isnumeric():  # isnumeric returns false for floats as '.' is not numeric
                strin[ii] = int(vv)
            else:
                strin[ii] = float(vv)
        except ValueError:
            strin[ii] = nan

    if pack:
        return strin[0]
    elif t2l:
        return tuple(strin)
    else:
        return strin
