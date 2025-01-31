import logging
import os
import datetime
import colorlog
import config
LOG_FORMAT = "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s"


# Function to set up the logger
def setup_logger(log_dir_path: str) -> logging.Logger:
    # Create a logger
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.DEBUG)  # Set the logging level

    # Create a file handler for logging to a file
    os.makedirs(log_dir_path, exist_ok=True)

    timestamp = datetime.datetime.now().isoformat().replace(":", "_").replace(".", "_").replace("-", "_")
    file_handler = logging.FileHandler(os.path.join(log_dir_path, f'server_{timestamp}.log'), mode='w')
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # Create a stream handler for logging to the console
    stream_handler = colorlog.StreamHandler()
    stream_formatter = colorlog.ColoredFormatter(LOG_FORMAT)
    stream_handler.setFormatter(stream_formatter)

    # Add both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


# Setup the logger
config = config.Config()
logger = setup_logger(config.logPath)

