import logging
import datetime


class Logger:
    logger = None
    def get_instance():
        if Logger.logger == None:
            now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            Logger.logger = logging.getLogger()
            Logger.logger.setLevel(logging.INFO)

            formatter = logging.Formatter(
                f'{now} [%(levelname)s] - %(message)s')
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            Logger.logger.addHandler(stream_handler)
        return Logger.logger


def info(*args):
    _log('INFO', *args)


def debug(*args):
    _log('DEBUG', *args)


def warning(*args):
    _log('WARNING', *args)


def error(*args):
    _log('ERROR', *args)


def _log(level: str, *args):
    desc = " ".join([str(i) for i in args])
    logger = Logger.get_instance()
    if level == 'INFO':
        logger.info(desc)
    elif level == 'DEBUG':
        logger.debug(desc)
    elif level == 'WARNING':
        logger.warning(desc)
    elif level == 'ERROR':
        logger.error(desc)
    else:
        raise RuntimeError('Undefined loglevel.')
