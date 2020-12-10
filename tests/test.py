# -------------------------------
# -*- coding: utf-8 -*-
# @Author：jianghan
# @Time：2020/12/7 18:41
# @File: test.py.py
# Python版本：3.6.8
# -------------------------------


import os
from datetime import time
import shutil

base_dir = os.path.dirname(os.path.abspath(__file__))

dir_list = ['file_log', 'time_minute_log', 'time_hour_log', 'time_day_log', 'time_midnight_log']

for dir_name in dir_list:
    if os.path.exists(os.path.join(base_dir, dir_name)):
        shutil.rmtree(os.path.join(base_dir, dir_name))
    os.mkdir(os.path.join(base_dir, dir_name))


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
            'class': 'pyloghandlers.handles.PylogRotatingFileHandler',
            'formatter': 'default',
            'filename': os.path.join(base_dir, 'file_log', 'info.log'),
            'max_bytes': 1024*1024,
            'backup_count': 100,
        },
        'time_minute': {
            'level': 'DEBUG',
            'class': 'pyloghandlers.handles.PylogTimedRotatingFileHandler',
            'formatter': 'default',
            'filename': os.path.join(base_dir, 'time_minute_log', 'info.log'),
            'when': 'h',
            'interval': 2,
            'backup_count': 100,
            'encoding': 'utf-8',
        },
        'time_hour': {
            'level': 'DEBUG',
            'class': 'pyloghandlers.handles.PylogTimedRotatingFileHandler',
            'formatter': 'default',
            'filename': os.path.join(base_dir, 'time_hour_log', 'info.log'),
            'when': 'h',
            'interval': 2,
            'backup_count': 100,
            'encoding': 'utf-8'
        },
        'time_day': {
            'level': 'DEBUG',
            'class': 'pyloghandlers.handles.PylogTimedRotatingFileHandler',
            'formatter': 'default',
            'filename': os.path.join(base_dir, 'time_day_log', 'info.log'),
            'when': 'd',
            'interval': 1,
            'backup_count': 100,
            'encoding': 'utf-8',
            'at_time': time(1, 0, 0)
        },
        'time_midnight': {
            'level': 'DEBUG',
            'class': 'pyloghandlers.handles.PylogTimedRotatingFileHandler',
            'formatter': 'default',
            'filename': os.path.join(base_dir, 'time_midnight_log', 'info.log'),
            'when': 'midnight',
            'interval': 1,
            'backup_count': 100,
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        'my_app': {
            'handlers': ['file', 'time_minute', 'time_hour', 'time_day', 'time_midnight'],
            'level': 'DEBUG',
        },
    }
}

from multiprocessing import Process


def write_log(tag):

    import time
    import logging.config

    logging.config.dictConfig(LOGGING)
    logger = logging.getLogger('my_app')

    _count = 0
    while True:
        _count += 1
        time.sleep(0.001)
        logger.info(f'[{str(tag)*4}] process tag {_count}')


if __name__ == '__main__':

    p_count = 6
    p_list = []
    for i in range(p_count):
        p_list.append(Process(target=write_log, args=(i+1,)))

    for p in p_list:
        p.start()

    for p in p_list:
        p.join()
