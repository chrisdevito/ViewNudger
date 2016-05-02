import logging


def myLogger(debug=False):
    """
    Creates a logger object.

    :param debug: (bool) Sets logging to level DEBUG or not.

    Returns:
        (logger object)

    Raises:
        None
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
