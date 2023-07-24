import unittest
from unittest.mock import MagicMock, patch

import pytest
from opyoid import Module
from opyoid.injector import Injector
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from gpyt_commandbus.injection.modules.session import SessionModule
from gpyt_commandbus.interface.settings import Settings


@pytest.fixture
def settings():
    mock_settings = MagicMock(spec=Settings)
    mock_settings.db_dsn = "sqlite:///:memory:"
    mock_settings.db_echo = True
    return mock_settings


@pytest.fixture
def settings_module(settings):
    class MockSettingsModule(Module):
        def configure(self) -> None:
            self.bind(Settings, to_instance=settings)

    return MockSettingsModule


@pytest.fixture
def engine():
    mock_engine = MagicMock(spec=Engine)
    return mock_engine


@pytest.fixture
def engine_module(engine):
    class MockEngineModule(Module):
        def configure(self) -> None:
            self.bind(Engine, to_instance=engine)

    return MockEngineModule


class SessionModuleTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self, settings_module, engine_module, engine):
        self.settings_module = settings_module
        self.engine_module = engine_module
        self.engine = engine

    def test_configure(self):
        # Arrange
        module = SessionModule()
        session_maker = MagicMock(spec=sessionmaker)
        mock_session = MagicMock(spec=Session)
        session_maker.return_value.return_value = mock_session

        with patch(
            "gpyt_commandbus.injection.modules.session.sessionmaker", session_maker
        ):
            injector = Injector([module, self.settings_module, self.engine_module])

            # Act
            session = injector.inject(Session)

            # Verify binding indirectly
            try:
                injector.inject(Session)
            except Exception as e:
                self.fail(f"Failed to inject Session: {e}")

        # Assert
        session_maker.assert_called_once_with(bind=self.engine)
        self.assertEqual(session, mock_session)
