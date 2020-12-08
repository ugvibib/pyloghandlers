
## PylogTimedRotatingFileHandler 使用

###### 一份完整的 PylogTimedRotatingFileHandler 配置使用如下

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
            'class': 'pyloghandlers.handlers.PylogTimedRotatingFileHandler',
            'formatter': 'default', # 日志文件内容格式化方式
            'filename': 'info.log', # 日志文件存储路径
            'mode': 'a',            # 日志文件操作模式 默认 'a'
            'encoding': 'utf-8',    # 日志文件写入编码方式 默认 None
            'terminator': '\n',     # 日志文件内容换行符 默认 '\n'
            'backup_count': 30,     # 日志文件最多备份数 默认 0
            'when': 'h',            # 按小时滚动， 默认 'h'， 详解见下
            'interval': 1,          # 间隔，不同when不一样，详解见下
            'utc': False,           # 是否启动 utc 时区
            'at_time': None,        # 指定滚动时间点，默认None 详解见下
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

###### 部分配置字段解释

> ##### when

`when` 可选项有:

- 秒 `s`
- 分钟 `m`
- 小时 `h`
- 天 `D`
- 午夜 `MIDNIGHT`
- 周 `w0`、`w1`、`w2`、`w3`、`w4`、`w5`、`w6`

特别说明
- `when` 不区分大小写
- `w0`~`w6`分别对应`Mon`~`Sun`
- `when` 等于 `s`时，这里的1个`interval`是`5s`，并非是 `1s`
- 以下文档中，当`when` 等于`星期`举例匀是以`when='w0'`为例


> ##### interval

为了多进程下，不同进程间文件命令规则一致。 对`interval`要求如下：

- 当`when`等于`s`、`m`、`h`时，每个间隔的秒数必须可以被`24*60*60`的结果整除，否则会报错；
- 当`when`等于`d`、`MIDNIGHT`、`w0`时，`interval`强制等于`1`，即使配置里面等于其他值也是如此； 


`interval` 默认值设置

- `when='s'` 时，默认 `interval=5`
- `when='m'` 时，默认 `interval=1`
- `when='h'` 时，默认 `interval=1`
- `when='d'` 时，强制 `interval=1`
- `when='MIDNIGHT'` 时，强制 `interval=1`
- `when='w0'` 时，强制 `interval=1`

例如：
```python
# 只有当除余为整数时才有效
handler1 = {'when': 's', 'interval': 1}
# interval有效，因为 (24*60*60) % (5*1) = 0

handler2 = {'when': 's', 'interval': 21}
# interval无效，因为 (24*60*60) % (5*21) = 90

handler3 = {'when': 'm', 'interval': 2}
# interval有效，因为 (24*60*60) % (60*2) = 0

handler4 = {'when': 'm', 'interval': 11}
# interval无效，因为 (24*60*60) % (60*11) = 600

handler5 = {'when': 'h', 'interval': 3}
# interval有效，因为 (24*60*60) % (60*60*3) = 0

handler6 = {'when': 'h', 'interval': 5}
# interval无效，因为 (24*60*60) % (60*60*5) = 14400
```

> ##### at_time

- `at_time` 值只在`when='d'` 或 `when='w0'` 时生效
-  `at_time` 参数类型为`time`类型

[完]