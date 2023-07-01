from typing import Dict, List

from pydantic import BaseSettings, PyObject

from gpyt_commandbus.interface.settings import Settings as ICommandBusSettings
from gpyt_commandbus.resources.hello import Hello


class Settings(BaseSettings, ICommandBusSettings):
    resources: List[Dict[str, PyObject]] = [
        {"/hello": Hello},
    ]

    class Config:
        env_prefix = "GPYT_"
        env_file = ".env"
