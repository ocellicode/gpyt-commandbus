from typing import Dict, List

from pydantic import BaseSettings, PyObject

from gpyt_commandbus.interface.settings import Settings as ICommandBusSettings
from gpyt_commandbus.resources.command import Command
from gpyt_commandbus.resources.target import Target


class Settings(BaseSettings, ICommandBusSettings):
    resources: List[Dict[str, PyObject]] = [
        {"/target": Target},
        {"/command": Command},
    ]
    db_dsn: str = "sqlite:///gpyt_commandbus.db"
    db_echo: bool = True
    log_level: str = "INFO"

    class Config:
        env_prefix = "GPYT_"
        env_file = ".env"
