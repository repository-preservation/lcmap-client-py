import logging

import six

from termcolor import colored


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


class Formatter(logging.Formatter):

    custom_date_format = '%Y.%m.%d %H:%M:%S'
    custom_timestamp_format = '%(asctime)s.%(msecs)d'
    custom_module_format = '%(name)s'
    custom_process_format = '[%(processName)s]'
    custom_level_format = '%(levelname)s'
    custom_record_format = '{} {} {} {} - %(message)s'
    usesTime = lambda _: True

    def format(self, record, fmt=None):
        if not fmt:
            fmt = self.custom_record_format.format(
                self.custom_timestamp_format,
                self.custom_process_format,
                self.custom_level_format,
                self.custom_module_format)
        self.update_style(fmt)
        self._fmt = fmt
        return logging.Formatter.format(self, record)

    def update_style(self, fmt):
        if six.PY2:
            return
        self._style = logging._STYLES['%'][0](fmt)

    def formatTime(self, record, datefmt=None):
        if not datefmt:
            datefmt = self.custom_date_format
        return logging.Formatter.formatTime(self, record, datefmt)


class ColoredFormatter(Formatter):

    custom_timestamp_format = colored(
        Formatter.custom_timestamp_format, 'green')
    custom_module_format = colored(Formatter.custom_module_format, 'yellow')
    custom_process_format = colored(Formatter.custom_process_format, 'cyan')

    def format(self, record=""):
        if record.levelno == logging.INFO:
            self.custom_level_format = colored(
                Formatter.custom_level_format, 'blue')
        elif record.levelno == logging.WARNING:
            self.custom_level_format = colored(
                Formatter.custom_level_format, 'yellow', attrs=['bold'])
        elif record.levelno in [logging.ERROR, logging.CRITICAL]:
            self.custom_level_format = colored(
                Formatter.custom_level_format, 'red')
        else:
            self.custom_level_format = colored(
                Formatter.custom_level_format, 'green', attrs=['bold'])
        return Formatter.format(self, record)

    def formatException(self, exec_info):
        formatted = Formatter.formatException(self, exec_info)
        return colored(formatted, 'red')


def configure(cfg):
    level = cfg.get_log_level()
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    if cfg.colored_logs:
        handler.setFormatter(ColoredFormatter())
    else:
        handler.setFormatter(Formatter())
    logger.addHandler(handler)
    if level == "none":
        logger.propagate = False
    else:
        logging.getLogger().setLevel(level)
        log.debug("Logging configured with level {}".format(level))
