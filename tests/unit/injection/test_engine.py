import unittest
from unittest.mock import MagicMock

import pytest
from opyoid import Injector, Module, SingletonScope
from sqlalchemy.engine import Engine

from gpyt_commandbus.injection.modules.engine import EngineModule
from gpyt_commandbus.interface.settings import Settings


@pytest.fixture
def settings():
    mock_settings = MagicMock(spec=Settings)
    mock_settings.db_dsn = "sqlite:///:memory:"
    mock_settings.db_echo = True
    return mock_settings


@pytest.fixture
def module(settings):
    class MockSettingsModule(Module):
        def configure(self) -> None:
            self.bind(Settings, to_instance=settings)

    return MockSettingsModule


class EngineModuleTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self, settings, module):
        self.settings = settings
        self.module = module

    def test_get_engine(self):
        # Arrange
        module = EngineModule()

        # Act
        engine = module.get_engine(self.settings)

        # Assert
        self.assertIsInstance(engine, Engine)
        self.assertEqual(str(engine.url), self.settings.db_dsn)
        self.assertEqual(engine.echo, self.settings.db_echo)

    def test_configure(self):
        # Arrange
        module = EngineModule()
        injector = Injector([module, self.module])

        # Act
        engine = injector.inject(Engine)

        # Assert
        self.assertIsInstance(engine, Engine)

        # Verify binding indirectly
        try:
            injector.inject(Engine)
        except Exception as e:
            self.fail(f"Failed to inject Engine: {e}")
