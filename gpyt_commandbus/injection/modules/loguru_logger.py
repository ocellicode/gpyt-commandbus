from logging import Logger
from sys import stderr

from loguru import logger
from opyoid import Module, SingletonScope


class LoguruModule(Module):
    @staticmethod
    def get_logger() -> Logger:
        logger.remove()
        logger.add(stderr, level="INFO")
        return logger  # type: ignore

    def configure(self) -> None:
        self.bind(Logger, to_provider=self.get_logger, scope=SingletonScope)
