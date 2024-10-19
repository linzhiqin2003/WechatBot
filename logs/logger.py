import logging
import os
import sys

class Logger:
    def __init__(self):
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.DIR = os.path.dirname(os.path.abspath(__file__))
        self.filePath = os.path.join(self.DIR, 'token_usage.log')

    def init_fileHd(self):
        fileHandler = logging.FileHandler(self.filePath)
        fileHandler.setLevel(logging.INFO)
        fileHandler.setFormatter(self.formatter)
        fileHandler.encoding = 'utf-8'
        return fileHandler

    def init_streamHd(self):
        streamHandler = logging.StreamHandler(sys.stdout)
        streamHandler.setLevel(logging.DEBUG)
        streamHandler.setFormatter(self.formatter)
        return streamHandler


    def init_logger(self,logger_name):
        loggers = logging.getLogger(logger_name)
        loggers.setLevel(logging.DEBUG)

        if not loggers.handlers:
            loggers.addHandler(self.init_fileHd())
            loggers.addHandler(self.init_streamHd())

        return loggers


logger = Logger().init_logger(logger_name="WeChat.log")



