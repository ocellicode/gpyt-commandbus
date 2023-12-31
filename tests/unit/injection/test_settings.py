import unittest

from opyoid.injector import Injector
from opyoid.utils import InjectedT

from gpyt_commandbus.injection.modules.settings import SettingsModule
from gpyt_commandbus.interface.settings import Settings as ISettings
from gpyt_commandbus.settings import Settings


class TestSettingsModule(unittest.TestCase):
    def test_configure(self):
        # Create the injector and bind the SettingsModule
        injector = Injector([SettingsModule])

        # Retrieve an instance of the bound interface
        settings: InjectedT[ISettings] = injector.inject(ISettings)

        # Assert that the instance is of the correct type
        self.assertIsInstance(settings, Settings)
