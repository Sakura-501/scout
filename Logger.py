import sys
import os
import time


# 控制台输出记录到文件
class Logger(object):
    def __init__(self, file_name="Default.log", stream=sys.stdout):
        self.terminal = stream
        self.log = open(file_name, "a")

    def write(self, message):
        try:
            self.terminal.write(message)
            self.log.write(message)
        except:
            self.log.write("cannot log message")

    def flush(self):
        pass