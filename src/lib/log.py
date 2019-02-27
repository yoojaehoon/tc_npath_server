import logging
import logging.handlers

def prepare_log(filename, level=logging.INFO):
    log = logging.getLogger(filename)
    handler = logging.handlers.RotatingFileHandler(filename, 'a', 10000, 5)
    fmt = logging.Formatter('%(asctime)s: %(message)s', "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(fmt)
    log.addHandler(handler)
    log.setLevel(level)
    return log
