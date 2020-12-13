import logging
from logging.config import fileConfig
from os import path

class LoggerUtil:

    def __init__(self):
        log_path = "config/logger_config.ini"
        log_file_path = path.join(path.dirname(path.abspath(__file__)), log_path)
        print(log_file_path)
        fileConfig(log_file_path)

    def getSelfLogger(self, logger_name):
        print(logger_name, "开始记录日志-----------")
        logger = logging.getLogger(logger_name)
        return logger