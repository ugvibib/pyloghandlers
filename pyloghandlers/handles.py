# -------------------------------
# -*- coding: utf-8 -*-
# @Author：jianghan
# @Time：2020/12/7 18:36
# @File: handles.py
# Python版本：3.6.8
# -------------------------------



"""
log 配置加载的时候，handler类只会实例化 1 次， 每次log打印，均不会再次实例化
"""


import io
import os
import re
import time
import shutil
import random
from stat import ST_MTIME

from portalocker import LOCK_EX, lock, unlock       # LOCK_EX: 独占锁
from logging.handlers import BaseRotatingHandler


_MIDNIGHT = 60*60*24


class BaseLockRotatingHandler(BaseRotatingHandler):

    def __init__(self, filename, mode='a', encoding=None, terminator="\n"):
        super().__init__(filename, mode, encoding=encoding, delay=True)

        self.terminator = terminator

        self.stream = None
        self.lock_stream = None
        self.lock_filename = self.get_lock_filename()
        self.is_locked = False

    def get_lock_filename(self):
        """ 返回 lock_filename 文件路径 """
        lock_file = f"{self.baseFilename}.lock"
        lock_path, lock_name = os.path.split(lock_file)
        lock_name = ".__" + lock_name
        return os.path.join(lock_path, lock_name)

    def do_open(self, mode=None):

        if mode is None:
            mode = self.mode

        stream = io.open(self.baseFilename, mode=mode, encoding=self.encoding)
        return stream

    def do_close(self):
        """ 关闭文件流 """
        if not self.stream:
            return

        try:
            if not self.stream.closed:
                self.stream.flush()
                self.stream.close()
        finally:
            self.stream = None

    def do_lock(self):
        """ 文件加锁 """
        if self.is_locked:
            print('self.is_locked is already True')
            return

        if not self.lock_stream or self.lock_stream.close():
            self.lock_stream = open(self.lock_filename, "wb", buffering=0)

        for i in range(10):
            # noinspection PyBroadException
            try:
                lock(self.lock_stream, LOCK_EX)
                self.is_locked = True
                break
            except Exception:
                continue
        else:
            raise RuntimeError("Cannot acquire lock after 10 attempts")

    def do_unlock(self):
        """ 文件解锁 """
        if not self.lock_stream:
            print('No self.stream_lock to unlock')
            return

        if self.is_locked:
            try:
                unlock(self.lock_stream)
            finally:
                self.is_locked = False
                self.lock_stream.close()
                self.lock_stream = None

    def do_write(self, record):

        self.stream = self.do_open()
        record += self.terminator

        try:
            self.stream.write(record)
        except UnicodeError:
            try:
                encoding = getattr(self.stream, 'encoding', self.encoding or 'us-ascii')
                msg_bin = record.encode(encoding, errors='ignore')
                msg = msg_bin.decode(encoding, errors='ignore')
                self.stream.write(msg)
            except UnicodeError:
                raise

        self.stream.flush()
        self.do_close()

    def emit(self, record):
        try:
            record = self.format(record)
            try:
                self.do_lock()
                try:
                    if self.should_rollover(record):
                        self.do_rollover()
                except Exception as e:
                    print(f'Unable to do rollover: {e}')
                self.do_write(record)
            finally:
                self.do_unlock()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)

    def should_rollover(self, record):
        raise NotImplementedError('[def shouldRollover] Must be inherited!')

    def do_rollover(self):
        raise NotImplementedError('[def do_rollover] Must be inherited!')

    def before_do_rollover(self):
        """ 执行滚动前的操作 """
        self.do_close()
        self.backup_count = getattr(self, 'backup_count', 0)
        if self.backup_count <= 0:
            # 这里的操作相当于清空了当前的log文件
            self.stream = self.do_open("w")
            self.do_close()
            return False

        # 尝试重命名，是否可正常重命名
        tmp_name = None
        while not tmp_name or os.path.exists(tmp_name):
            tmp_name = f'{self.baseFilename}.rotate.{random.getrandbits(64)}'
        try:
            shutil.copyfile(self.baseFilename, tmp_name)
        except (IOError, OSError) as e:
            print(f'Log file is using: {e}')
            return False

        os.remove(tmp_name)
        return True

    def _open(self):
        """ 屏蔽系统自带的 open 操作， 使用自己创建的 open """
        pass

    def flush(self):
        """ 屏蔽系统自带的 flush 操作 """
        pass

    def close(self):
        """ 重新系统 close 操作 """
        try:
            self.do_close()
        finally:
            super().close()


class PylogRotatingFileHandler(BaseLockRotatingHandler):

    def __init__(self, filename, mode='a', encoding=None, terminator='\n', max_bytes=0, backup_count=0):

        if max_bytes > 0:
            mode = 'a'

        super().__init__(filename, mode=mode, encoding=encoding, terminator=terminator)

        self.max_bytes = max_bytes
        self.backup_count = backup_count

    def should_rollover(self, record):
        """ 判断是否应该滚动日志文件 """
        if self.max_bytes <= 0:
            return False

        self.stream = self.do_open()
        try:
            self.stream.seek(0, 2)
            if self.stream.tell() + len(f'{record}\n') >= self.max_bytes:
                return True
        finally:
            self.do_close()
        return False

    def do_rollover(self):
        """ 文件滚动 """
        _continue= self.before_do_rollover()
        if not _continue:
            return

        # 执行文件滚动操作
        for i in range(self.backup_count - 1, 0, -1):
            sfn = self.rotation_filename("%s.%d" % (self.baseFilename, i))
            dfn = self.rotation_filename("%s.%d" % (self.baseFilename, i + 1))
            if os.path.exists(sfn):
                if os.path.exists(dfn):
                    os.remove(dfn)
                os.rename(sfn, dfn)
        dfn = self.rotation_filename(self.baseFilename + ".1")
        if os.path.exists(dfn):
            os.remove(dfn)
        self.rotate(self.baseFilename, dfn)


class PylogTimedRotatingFileHandler(BaseLockRotatingHandler):

    def __init__(self, filename, mode='a', encoding=None, terminator='\n', backup_count=0, when='h', interval=1, utc=False, at_time=None):
        super().__init__(filename=filename, mode=mode, encoding=encoding, terminator=terminator)
        self.when = when.upper()
        self.backup_count = backup_count
        self.utc = utc
        self.at_time = at_time

        if self.when == 'S':
            self.interval = 5
            self.suffix = "%Y-%m-%d_%H-%M-%S"
            self.ext_match = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}(\.\w+)?$"

        elif self.when == 'M':
            self.interval = 60  # one minute
            self.suffix = "%Y-%m-%d_%H-%M"
            self.ext_match = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}(\.\w+)?$"

        elif self.when == 'H':
            self.interval = 60 * 60
            self.suffix = "%Y-%m-%d_%H"
            self.ext_match = r"^\d{4}-\d{2}-\d{2}_\d{2}(\.\w+)?$"

        elif self.when == 'D' or self.when == 'MIDNIGHT':
            if interval != 1:
                print(f'Interval only supported equal to 1 when {self.when}')
                interval = 1

            if self.when == 'MIDNIGHT':
                self.at_time = None

            self.interval = 60 * 60 * 24
            self.suffix = "%Y-%m-%d"
            self.ext_match = r"^\d{4}-\d{2}-\d{2}(\.\w+)?$"

        elif self.when.startswith('W'):
            if interval != 1:
                print(f'Interval only supported equal to 1 when {self.when}')
                interval = 1
            if len(self.when) != 2:
                raise ValueError("You must specify a day for weekly rollover from 0 to 6 (0 is Monday): %s" % self.when)
            if self.when[1] < '0' or self.when[1] > '6':
                raise ValueError("Invalid day specified for weekly rollover: %s" % self.when)

            self.interval = 60 * 60 * 24 * 7
            self.suffix = "%Y-%m-%d"
            self.ext_match = r"^\d{4}-\d{2}-\d{2}(\.\w+)?$"
            self.day_of_week = int(self.when[1])
        else:
            raise ValueError("Invalid rollover interval specified: %s" % self.when)

        self.ext_match = re.compile(self.ext_match, re.ASCII)
        self.interval = self.interval * interval
        if self.when in ['S', 'M', 'H'] and _MIDNIGHT % interval != 0:
            ValueError(f'Invalid rollover interval specified: {interval}')

        if os.path.exists(filename):
            t = os.stat(filename)[ST_MTIME]
        else:
            t = int(time.time())
        self.rollover_at = self.compute_rollover(t)

    def should_rollover(self, record):
        t = int(time.time())
        if t >= self.rollover_at:
            return True
        return False

    def do_rollover(self):
        """ 执行滚动 """
        _continue = self.before_do_rollover()
        if not _continue:
            return
        current_time = int(time.time())
        t = self.rollover_at - self.interval
        if self.utc:
            time_tuple = time.gmtime(t)
        else:
            time_tuple = time.localtime(t)
        dfn = self.rotation_filename(self.baseFilename + "." + time.strftime(self.suffix, time_tuple))

        if not os.path.exists(dfn):
            self.rotate(self.baseFilename, dfn)

        for s in self.get_files_to_delete():
            os.remove(s)

        new_rollover_at = self.compute_rollover(current_time)
        while new_rollover_at <= current_time:
            new_rollover_at += self.interval
        self.rollover_at = new_rollover_at

    def get_files_to_delete(self):
        """ 获取待删除的 log路径 """
        dir_name, base_name = os.path.split(self.baseFilename)
        file_names = os.listdir(dir_name)
        result = []
        prefix = base_name + "."
        plen = len(prefix)
        for file_name in file_names:
            if file_name[:plen] == prefix:
                suffix = file_name[plen:]
                if self.ext_match.match(suffix):
                    result.append(os.path.join(dir_name, file_name))
        if len(result) < self.backup_count:
            result = []
        else:
            result.sort()
            result = result[:len(result) - self.backup_count]
        return result

    def compute_rollover(self, current_time):
        """ 根据指定的时间计算出滚动时间 """
        current_time = int(current_time)    # 时间戳取整

        if self.utc:
            t = time.gmtime(current_time)
        else:
            t = time.localtime(current_time)

        # 当前时间所在日期对应的时间戳
        current_day = time.mktime(time.strptime(f'{t.tm_year}-{t.tm_mon}-{t.tm_mday}', '%Y-%m-%d'))

        # 时 / 分 / 秒
        if self.when in ('S', 'M', 'H'):
            r = current_time - current_day
            r_integer = r // self.interval      # 取整
            # r_remainder = r % self.interval     # 取余
            result = current_day + self.interval * (r_integer + 1)

        # 天 / 午夜
        elif self.when in ('D', 'MIDNIGHT'):
            if self.at_time:
                r = (self.at_time.hour*60 + self.at_time.minute)*60 + self.at_time.second
                result = current_day + r
            else:
                result = current_day

            if result < current_time:
                result += self.interval
        # 周
        else:
            current_day_of_week = t[6]      # current_time 处于一周的第n天, 0是周一
            first_day_of_week = current_day - current_day_of_week*_MIDNIGHT     # 一周的起始时间戳
            result = first_day_of_week + self.day_of_week*_MIDNIGHT     # 一周设定的滚动日期
            if self.at_time:
                r = (self.at_time.hour * 60 + self.at_time.minute) * 60 + self.at_time.second
                result += r     # 滚动日期设定的滚动时间
            if result < current_time:
                result += self.interval
        return result
