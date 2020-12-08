# -------------------------------
# -*- coding: utf-8 -*-
# @Author：jianghan
# @Time：2020/12/7 18:41
# @File: test.py.py
# Python版本：3.6.8
# -------------------------------


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'log_handlers.PyLogRotatingFileHandler',
            # 'class': 'log_handler_concurrent.ConcurrentRotatingFileHandler',
            'formatter': 'default',
            'filename': 'info.log',
            'max_bytes': 1024,
            'backup_count': 5,
        },
        'time': {
            'level': 'DEBUG',
            'class': 'log_handlers.PyLogTimedRotatingFileHandler',
            'formatter': 'default',
            'filename': 'info.log',
            'when': 'S',
            'interval': 1,
            'backup_count': 100,
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        'root': {
            'handlers': ['time'],
            # 'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}

from multiprocessing import Process


def write_log(tag):

    import logging.config
    logging.config.dictConfig(LOGGING)
    logger = logging.getLogger('root')

    for i in range(0, 10000):
        # import time
        # time.sleep(0.001)
        logger.debug(f'[{str(tag)*2}] process tag {i}')


if __name__ == '__main__':

    p_count = 4
    p_list = []
    for i in range(p_count):
        p_list.append(Process(target=write_log, args=(i+1,)))

    for p in p_list:
        p.start()

    for p in p_list:
        p.join()
