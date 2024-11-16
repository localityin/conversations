import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

# Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
log_filename = os.path.join(LOG_DIR, f"locality-inference_{datetime.now().strftime('%Y-%m-%d')}.log")
logger = logging.getLogger("locality_inference")
logger.setLevel(logging.DEBUG)

# File handler with rotation
file_handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1)
file_handler.suffix = "%Y-%m-%d"
file_handler.setLevel(logging.DEBUG)

# Console handler for debugging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Utility function to log messages
def log_message(level, message):
    if level.lower() == "debug":
        logger.debug(message)
    elif level.lower() == "info":
        logger.info(message)
    elif level.lower() == "warning":
        logger.warning(message)
    elif level.lower() == "error":
        logger.error(message)
    elif level.lower() == "critical":
        logger.critical(message)