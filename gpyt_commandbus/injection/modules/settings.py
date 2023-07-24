from opyoid import Module, SingletonScope

from gpyt_commandbus.interface.settings import Settings as ISettings
from gpyt_commandbus.settings import Settings


class SettingsModule(Module):
    def configure(self) -> None:
        self.bind(ISettings, to_class=Settings, scope=SingletonScope)
