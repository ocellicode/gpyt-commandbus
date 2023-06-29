"""
Test gpyt_commandbus.injection.modules.settings
"""

from abc import ABC

from hamcrest import assert_that, is_

from gpyt_commandbus.interface.settings import Settings as ISettings


def test_isettings_has_class_attributes():
    assert_that(ISettings.resources, is_(NotImplemented))


def test_isettiings_is_subclass_abc():
    assert_that(issubclass(ISettings, ABC), is_(True))
