import logging
from typing import Optional

class Logger:
    def __init__(self, path: str, file: bool, print: bool) -> None:
        self.setup_logger(path, file, print)

    def setup_logger(self, path:str, file: bool, print: bool):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        if file:
            file_handler = logging.FileHandler(path)
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        if print:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str, name: str="") -> None:
        message = name + message
        self.logger.info(message)

    def warning(self, message: str, name: str="") -> None:
        message = name + message
        self.logger.warning(message)

    def error(self, message: str, name: str="") -> None:
        message = name + message
        self.logger.error(message) 

    def exception(self, message: str, name: str="") -> None:
        message = name + message
        self.logger.exception(message) 


# Logger Test code
# Log = Logger('log/test.log')
# Log.info("Info Test")
# Log.error("Error Test")
