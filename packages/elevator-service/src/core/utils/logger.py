import logging

import colorlog


class Logger:
    def __init__(
        self,
        name=__name__,
        level=logging.DEBUG,
    ):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def get_logger(self):
        return self._logger


logger = Logger().get_logger()
