import logging
from core.env import BaseEnvironment

# Create a logger
logger = logging.getLogger("beachbooker_logger")
logger.setLevel(logging.DEBUG)

# Create a file handler
log_file = BaseEnvironment.load().write_folder() / "beachbooker.log"
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and set it for both handlers
formatter = logging.Formatter("%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
