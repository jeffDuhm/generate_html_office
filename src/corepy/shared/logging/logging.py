import logging

class Logger:
    
    def __init__(self, logger_name):
        self.logger_name = logger_name
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(self.logger_name)
    
    def info(self, data):
        self.logger.info(data)
    
    def debug(self, data):
        self.logger.debug(data)
    
    def warning(self, data):
        self.logger.warning(data)
    
    def error(self, data):
        self.logger.error(data)
    
    def critical(self, data):
        self.logger.critical(data)