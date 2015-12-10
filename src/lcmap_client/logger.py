import logging


log = logging.getLogger(__name__)


def serialize_level(name):
    name = name.lower()
    if name == "all":
        return logging.NOTSET
    if name in ["trace", "debug"]:
        return logging.DEBUG
    elif name == "info":
        return logging.INFO
    elif name in ["warn", "warning"]:
        return logging.WARNING
    elif name == "error":
        return logging.ERROR
    elif name in ["critical", "fatal", "none"]:
        return logging.CRITICAL


def configure(cfg):
    level = cfg.get_log_level()
    logging.basicConfig(
        datefmt='%Y.%m.%d %H:%M:%S',
        level=level,
        format='%(asctime)s %(levelname)s %(name)s - %(message)s')
    if level == "none":
        logging.getLogger().propagate = False
    else:
        logging.getLogger().setLevel(level)
        log.debug("Logging configured with level {}".format(level))
