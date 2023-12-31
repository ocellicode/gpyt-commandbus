from flask import Flask
from opyoid import Injector

from gpyt_commandbus.injection.modules.pydantic_loader import PydanticLoader

injector = Injector(PydanticLoader().module_list)  # type: ignore

app = injector.inject(Flask)
