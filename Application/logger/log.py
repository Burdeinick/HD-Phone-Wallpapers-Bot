import logging


class MyLogging:
    """The class for creating a logger."""
    def __init__(self):
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    def setup_logger(self, name, log_file, level=logging.ERROR):
        """This method returns a logger."""
        handler = logging.FileHandler(log_file)
        handler.setFormatter(self.formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        return logger