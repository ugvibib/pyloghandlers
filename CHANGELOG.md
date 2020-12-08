

##### v0.0.1

基于 [concurrent-log-handler v0.9.20](https://github.com/Preston-Landers/concurrent-log-handler) 作了以下改动

- 移除日志文件压缩功能
- 移除文件授权账号授权功能
- 移除 `python2.x` 的支持
- 移除 `debug` 功能
- 移除夏令时(基于 `logging.handlers`)
- 移除日志队列


- 方法名和属性名的重命名
- 类的重定义和重命名
- 加锁文件名定义逻辑
- 文件大小判断逻辑(还原 `logging.handlers` 逻辑)


- 增加时间滚动切割日志类 (基于 `logging.handlers`)
