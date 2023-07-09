from typing import List

from pydantic import BaseSettings, PyObject

from gpyt_commandbus.injection.modules.app import AppModule
from gpyt_commandbus.injection.modules.engine import EngineModule
from gpyt_commandbus.injection.modules.loguru_logger import LoguruModule
from gpyt_commandbus.injection.modules.session import SessionModule
from gpyt_commandbus.injection.modules.settings import SettingsModule


class PydanticLoader(BaseSettings):
    module_list: List[PyObject] = [
        SettingsModule,
        AppModule,
        LoguruModule,
        EngineModule,
        SessionModule,
    ]

    class Config:
        env_prefix = "GPYT_"
