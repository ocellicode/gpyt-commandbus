from opyoid import Module, SingletonScope
from sqlalchemy.engine import Engine, create_engine

from gpyt_commandbus.settings import Settings


class EngineModule(Module):
    @staticmethod
    def get_engine(settings: Settings) -> Engine:
        return create_engine(settings.db_dsn, echo=settings.db_echo)

    def configure(self) -> None:
        self.bind(Engine, to_provider=self.get_engine, scope=SingletonScope)
