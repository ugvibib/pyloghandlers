
## PylogRotatingFileHandler 使用

###### 一份完整的 PylogRotatingFileHandler 配置使用如下

```python
config = {
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
            'class': 'pyloghandlers.handlers.PyLogRotatingFileHandler',
            'formatter': 'default', # 日志文件内容格式化方式
            'filename': 'info.log', # 日志文件存储路径
            'mode': 'a',            # 日志文件操作模式 默认 'a'
            'encoding': 'utf-8',    # 日志文件写入编码方式 默认 None
            'max_bytes': 1024,      # 日志文件最大字节数 默认 0
            'backup_count': 30,     # 日志文件最多备份数 默认 0
            'terminator': '\n',     # 日志文件内容换行符 默认 '\n'
        },
    },
    'loggers': {
        'my_app': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}
```

###### 使用

```python
import logging.config

logging.config.dictConfig(config)       # config 日志配置字典
logger = logging.getLogger('my_app')

logger.info('this is a test info log record')
logger.debug('this is a test debug log record')

```