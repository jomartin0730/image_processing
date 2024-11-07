import logging
from typing import Optional

class Logger:   
    def __init__(self, path: str, name: str) -> None:
        self.log_path: str = path
        self.setup_logger(name)

    def setup_logger(self, name: str) -> None:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.FileHandler(self.log_path),
                logging.StreamHandler()
            ]
        )
        self.logger: logging.Logger = logging.getLogger(name)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message) 

    def exception(self, message: str) -> None:
        self.logger.exception(message) 


# Logger Test code
# Log = Logger('log/test.log')
# Log.info("Info Test")
# Log.error("Error Test")
