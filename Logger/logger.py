import logging
from logging.handlers import RotatingFileHandler

log_file = "Logger/logs/test.log"

def setup_logger():
  logger = logging.getLogger("testLogger")
  logger.setLevel(logging.DEBUG)

  console_handler = logging.StreamHandler()
  console_handler.setLevel(logging.INFO)
  console_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  console_handler.setFormatter(console_format)

  file_handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)
  file_handler.setLevel(logging.DEBUG)
  file_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  file_handler.setFormatter(file_format)

  logger.addHandler(console_handler)
  logger.addHandler(file_handler)

  return logger
  
logger = setup_logger()