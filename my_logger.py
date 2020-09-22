import logging.config
from logging import getLogger

# Логирование
LOGGING = {
    'disable_existing_loggers': True,
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s | %(module)s.%(funcName)s | %(asctime)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
logging.config.dictConfig(LOGGING)
logger = getLogger(__name__)


def debug_requests(f):
    def inner(*args, **kwargs):
        try:
            logger.debug(f'Обращение в функцию `{f.__name__}`')
            return f(*args, **kwargs)
        except Exception:
            logger.exception(f'Ошибка в функции `{f.__name__}`')
            raise
    return inner