from packaging import version

from gpyt_commandbus import __version__


def test_version():
    assert isinstance(version.parse(__version__), version.Version)
