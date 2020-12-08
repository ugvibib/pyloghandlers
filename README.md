

### pyloghandlers


`pyloghandlers` 是对`logging.handlers`中的类进行了继承重写，解决了在多进程下日志写入混乱的问题。 
这是[concurrent-log-handler](https://github.com/Preston-Landers/concurrent-log-handler)的简化版本，
引用里面的核心方法，去掉了一些多余功能， 支持上按时间切割类。


###### 变更汇总

- 删除
    - 移除日志文件压缩功能
    - 移除文件授权账号授权功能
    - 移除 `python2.x` 的支持
    - 移除 `debug` 功能
    - 移除夏令时(相比于 `logging.handlers`)
    - 移除日志队列
- 修改
    - 方法名和属性名的重命名
    - 类的重定义和重命名
    - 加锁文件名定义逻辑
    - 文件大小判断逻辑(还原成logging.handlers逻辑)
- 新增
    - 支持时间滚动(相比于logging.handlers有改动)


### Links

- [pyloghandlers on Github](https://github.com/ugvibib/pyloghandlers)
- [concurrent-log-handler on Github](https://github.com/Preston-Landers/concurrent-log-handler)


### Instructions and Usage

###### Installation
~~~linux
pip install pyloghandlers
~~~


### Simple Example

- `class PylogRotatingFileHandler` 的使用方法, 查看 [pylog_rotating_file_handler.md](https://github.com/ugvibib/pyloghandlers/docs/pylog_rotating_file_handler.md)
- `class PylogTimedRotatingFileHandler` 的使用方法, 查看 [pylog_timed_rotating_file_handler.md](https://github.com/ugvibib/pyloghandlers/docs/pylog_timed_rotating_file_handler.md)


### Changelog

查看 [CHANGELOG.md](https://github.com/ugvibib/pyloghandlers/CHANGELOG.md)


### License

查看 `License` 文件
