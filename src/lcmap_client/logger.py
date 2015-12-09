import logging


def serialize_level(name):
    name = name.lower()
    if name in ["all", "trace", "debug"]:
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
    logging.BasicConfig(
        format='%(asctime)s %(message)s',
        datefmt='%Y.%m.%d %I:%M:%S %P',
        level=cfg.get_log_level())
    logging.debug("Logging configured.")
