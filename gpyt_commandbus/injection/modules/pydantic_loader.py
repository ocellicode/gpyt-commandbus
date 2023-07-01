from typing import List

from pydantic import BaseSettings, PyObject

from gpyt_commandbus.injection.modules.app import AppModule
from gpyt_commandbus.injection.modules.settings import SettingsModule


class PydanticLoader(BaseSettings):
    module_list: List[PyObject] = [
        SettingsModule,
        AppModule,
    ]

    class Config:
        env_prefix = "GPYT_"
