import unittest
from unittest.mock import MagicMock, patch

from flask import Flask
from flask_restful import Api
from opyoid import SingletonScope
from sqlalchemy.orm import Session

from gpyt_commandbus.injection.modules.app import AppModule
from gpyt_commandbus.interface.settings import Settings


class TestAppModule(unittest.TestCase):
    def setUp(self):
        self.settings = MagicMock(spec=Settings)
        self.logger = MagicMock()
        self.session = MagicMock(spec=Session)

    def test_get_app(self):
        app_module = AppModule()

        # Mock resource settings
        resource_settings = {"/path1": MagicMock(), "/path2": MagicMock()}
        self.settings.resources = [resource_settings]

        # Mock Flask and Api objects
        mock_flask = MagicMock(spec=Flask)
        mock_api = MagicMock(spec=Api)

        # Mock add_resource method of the Api object
        mock_api.add_resource = MagicMock()

        # Patch the Flask and Api objects
        with patch(
            "gpyt_commandbus.injection.modules.app.Flask", return_value=mock_flask
        ), patch("gpyt_commandbus.injection.modules.app.Api", return_value=mock_api):
            # Call the get_app method
            app = app_module.get_app(self.settings, self.logger, self.session)

            # Assert that the Flask object is returned
            self.assertEqual(app, mock_flask)

            # Assert that add_resource is called for each resource
            for key, value in resource_settings.items():
                mock_api.add_resource.assert_any_call(
                    value,
                    key,
                    resource_class_kwargs={
                        "logger": self.logger,
                        "session": self.session,
                    },
                )

    def test_configure(self):
        app_module = AppModule()
        app_module.bind = MagicMock()

        # Call the configure method
        app_module.configure()

        # Assert that the bind method is called with the correct arguments
        app_module.bind.assert_called_with(
            Flask, to_provider=app_module.get_app, scope=SingletonScope
        )
