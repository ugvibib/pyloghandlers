

## pyloghandlers


> `pyloghandlers` 是对`logging.handlers`中的类进行了继承重写，解决了在多进程下日志写入混乱的问题。 
这是[concurrent-log-handler](https://github.com/Preston-Landers/concurrent-log-handler)的简化版本，
引用里面核心方法，删除一些多余功能， 增加按时间切割类


### 变更汇总


- 移除日志文件压缩功能
- 移除文件授权账号授权功能
- 移除 `python2.x` 的支持
- 移除 `debug` 功能
- 移除夏令时(基于 `logging.handlers`)
- 移除日志队列


- 方法名和属性名的重命名
- 类的重定义和重命名
- 加锁文件名定义逻辑
- 文件大小判断逻辑(还原成 `logging.handlers` 逻辑)


- 支持时间滚动(基于 `logging.handlers` 有改动)

tips:上面的变更汇总是pyloghandlers v0.0.1 相比于 concurrent-log-handler v0.9.20 的对比结果  



### 相关链接

- [pyloghandlers on Github](https://github.com/ugvibib/pyloghandlers)
- [concurrent-log-handler on Github](https://github.com/Preston-Landers/concurrent-log-handler)


### 安装与使用

###### 安装

~~~linux
pip install pyloghandlers
~~~

###### 使用

- `class PylogRotatingFileHandler` 的使用方法, 查看 [pylog_rotating_file_handler.md](https://github.com/ugvibib/pyloghandlers/blob/master/docs/pylog_rotating_file_handler.md)
- `class PylogTimedRotatingFileHandler` 的使用方法, 查看 [pylog_timed_rotating_file_handler.md](https://github.com/ugvibib/pyloghandlers//blob/master/docs/pylog_timed_rotating_file_handler.md)


### Changelog

查看 [CHANGELOG.md](https://github.com/ugvibib/pyloghandlers/blob/master/CHANGELOG.md)


### License

查看 [License](https://github.com/ugvibib/pyloghandlers/blob/master/LICENSE)


