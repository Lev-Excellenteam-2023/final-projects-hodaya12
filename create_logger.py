import logging
from logging.handlers import TimedRotatingFileHandler
import os

def create_logger(directory_path:str):
    """
       Create and configure a logger to handle log messages and store them in a rotating log file.

       :param directory_path: The path to the directory where log files will be stored.
       :return: A logger instance with the specified configuration.
       """
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create log formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create file handler and set formatter
    file_handler = TimedRotatingFileHandler(os.path.join(directory_path, 'logs.log'), when='midnight', interval=1, backupCount=5)

    file_handler.setFormatter(formatter)

    # Add file handler to logger
    logger.addHandler(file_handler)
    return logger
