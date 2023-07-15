import unittest
from logging import Logger
from sys import stderr
from unittest.mock import patch

from loguru import logger
from opyoid.injector import Injector

from gpyt_commandbus.injection.modules.loguru_logger import LoguruModule


class LoguruModuleTest(unittest.TestCase):
    def test_get_logger(self):
        # Arrange
        module = LoguruModule()

        # Act
        with patch.object(logger, "remove") as mock_remove, patch.object(
            logger, "add"
        ) as mock_add:
            result = module.get_logger()

        # Assert
        self.assertEqual(result, logger)
        mock_remove.assert_called_once()
        mock_add.assert_called_once_with(stderr, level="INFO")

    def test_configure(self):
        # Arrange
        module = LoguruModule()
        injector = Injector([module])

        # Act
        logger_instance = injector.inject(Logger)

        # Assert
        self.assertEqual(logger_instance, logger)

        # Verify binding indirectly
        try:
            injector.inject(Logger)
        except Exception as e:
            self.fail(f"Failed to inject Logger: {e}")
