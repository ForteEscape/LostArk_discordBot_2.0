import logging


class ExceptionHandler:
    def __init__(self, logger_name):
        self.__logger = self.make_logger(logger_name)

    def make_logger(self, name):
        formatter = logging.Formatter("[%(asctime)-10s] (줄 번호: %(lineno)d) %(name)s:%(levelname)s - %(message)s")

        logger = logging.getLogger(name=name)

        if len(logger.handlers) > 0:
            return logger

        logger.propagate = False
        logger.setLevel(logging.DEBUG)

        console = logging.StreamHandler()
        file_handler = logging.FileHandler("./data/logs/info.log")
        file_handler.setFormatter(formatter)

        console.setLevel(logging.INFO)
        file_handler.setLevel(logging.DEBUG)

        logger.addHandler(console)
        logger.addHandler(file_handler)

        return logger

    def get_logger(self):
        return self.__logger
