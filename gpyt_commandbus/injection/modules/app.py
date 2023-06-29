from flask import Flask
from flask_restful import Api
from opyoid import Module, SingletonScope

from gpyt_commandbus.settings import Settings


class AppModule(Module):
    @staticmethod
    def get_app(settings: Settings) -> Flask:
        app = Flask(__name__)
        api = Api(app)
        for res in settings.resources:
            for key, value in res.items():
                api.add_resource(
                    value,
                    key,
                )

        return app

    def configure(self) -> None:
        self.bind(Flask, to_provider=self.get_app, scope=SingletonScope)
