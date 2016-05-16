import logging


def myLogger(debug=False):
    """
    Creates a logger object.

    :param debug: Sets logging to level DEBUG.
    :type debug: (bool)

    :raises: None

    :return: logger
    :rtype: logger object
    """
    LFMT = '%(asctime)-15s %(name)s [%(levelname)s] %(message)s'
    DFMT = '%Y-%m-%d %H:%M:%S'
    FMT = logging.Formatter(LFMT, DFMT)
    shandler = logging.StreamHandler()
    shandler.setFormatter(FMT)
    log = logging.getLogger("ViewNudger")
    log.addHandler(shandler)

    if debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    log.propagate = False

    return log
