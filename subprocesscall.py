def subprocesscall(command, shell=False):
    """
    Function used to execute commands in the terminal. Prints any errors to logs
    :param command: Command to execute
    :param shell: Whether to use a virtual shell or not
    :return: stdout, stderr[, exitcode]

    Changelog:
    Corrections to better conform with Python conventions (20190708fakas)

    """

    from subprocess import Popen, PIPE, TimeoutExpired
    from shlex import split

    if not shell and type(command) is str:
        command = split(command)

    p = Popen(command, stdout=PIPE, stderr=PIPE, shell=shell)

    exitcode = None
    multiout = []
    multierr = []
    while exitcode is None:
        try:
            exitcode = p.wait(timeout=0.1)
        except TimeoutExpired:
            _stdout, _stderr = p.communicate()
            multiout.append(_stdout)
            multierr.append(_stderr)
        except Exception:
            raise
    try:
        stdout, stderr = p.communicate()
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")
    except ValueError:
        if len(multiout) > 0:
            for ii, vv in enumerate(multiout):
                multiout[ii] = vv.decode("utf-8")
            for ii, vv in enumerate(multierr):
                multierr[ii] = vv.decode("utf-8")
            stdout = "".join(multiout)
            stderr = "".join(multierr)
        else:
            raise
    except Exception:
        raise

    return str(stdout), str(stderr), exitcode
