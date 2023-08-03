import logging
from termcolor import colored

class ColoredFormatter(logging.Formatter):

    COLORS = {
        'INFO': 'green',
        'DEBUG': 'blue',
        'ERROR': 'red',
        'WARNING': 'yellow'
    }

    def format(self, record):
        log_level = colored("[{}]".format(record.levelname), self.COLORS.get(record.levelname, 'white'))
        formatted_time = colored(self.formatTime(record, self.datefmt).split(',')[0], 'grey')
        return "{} {} {}".format(formatted_time, log_level, record.getMessage())

# Setting up the logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s\t[%(levelname)s]\t%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger()
for handler in logger.handlers:
    handler.setFormatter(ColoredFormatter("%(asctime)s\t[%(levelname)s]\t%(message)s"))

# # Test out the logging
# logger.info("This is an info message.")
# logger.debug("This is a debug message.")
# logger.error("This is an error message.")
# logger.warning("This is a warning message.")