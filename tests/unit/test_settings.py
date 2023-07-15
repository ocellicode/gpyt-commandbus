import pytest

from gpyt_commandbus.resources.target import Target
from gpyt_commandbus.settings import Settings


@pytest.fixture
def settings():
    # note: values are read from pyproject.toml
    return Settings()


def test_default_values(settings):
    assert settings.db_dsn == "sqlite:///:memory:"
    assert settings.db_echo is True
    assert settings.resources == [{"/target": Target}]


def test_env_prefix(settings):
    assert settings.Config.env_prefix == "GPYT_"


def test_env_file(settings):
    assert settings.Config.env_file == ".env"
