import unittest
from unittest.mock import MagicMock

from flask import Flask
from flask_restful import Api
from loguru import logger
from sqlalchemy.orm import Session

from gpyt_commandbus.model.target import Target as TargetORM
from gpyt_commandbus.resources.target import Target
from gpyt_commandbus.resources.target.targetmodel import TargetModel


class TargetTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.session = MagicMock(spec=Session)
        self.api.add_resource(
            Target,
            "/target",
            resource_class_kwargs={"logger": logger, "session": self.session},
        )
        self.client = self.app.test_client()

    def test_post_target_valid_request(self):
        target_data = {"name": "example", "url": "http://example.com"}
        response = self.client.post("/target", json=target_data)
        self.assertEqual(response.status_code, 201)

        # Verify that the TargetModel object was created correctly
        expected_target_model = TargetModel(**target_data)

        # Verify that the TargetORM object was created and added to the session correctly
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()

        # Verify that the response data matches the TargetModel
        response_data = response.get_json()
        expected_data = expected_target_model.dict()
        self.assertEqual(response_data, expected_data)

    def test_post_target_invalid_request(self):
        target_data = {"name": "example", "invalid_key": "http://example.com"}
        response = self.client.post("/target", json=target_data)
        self.assertEqual(response.status_code, 400)

        # Verify that the error message is returned
        response_data = response.get_json()
        self.assertEqual(response_data, {"message": "Invalid request"})

        # Verify that the session methods were not called
        self.session.add.assert_not_called()
        self.session.commit.assert_not_called()

    def test_post_target_error(self):
        target_data = {"name": "example", "url": "http://example.com"}
        self.session.commit.side_effect = Exception("Test error")
        response = self.client.post("/target", json=target_data)
        self.assertEqual(response.status_code, 500)

        # Verify that the error message is returned
        response_data = response.get_json()
        self.assertEqual(response_data, {"message": "Error"})

        # Verify that the session methods were called
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()

    def test_verify_request_valid(self):
        target_data = {"name": "example", "url": "http://example.com"}
        target = Target(logger=logger, session=self.session)
        result = target.verify_request(target_data)
        self.assertIsInstance(result, TargetModel)

    def test_verify_request_invalid(self):
        target_data = {"name": "example", "invalid_key": "http://example.com"}
        target = Target(logger=logger, session=self.session)
        result = target.verify_request(target_data)
        self.assertFalse(result)

    def test_persist_target(self):
        target_data = {"name": "example", "url": "http://example.com"}
        target_model = TargetModel(**target_data)
        target = Target(logger=logger, session=self.session)

        target.persist_target(target_model)

        # Verify that the session add and commit methods were called
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()

        # Get the persisted TargetORM object from the session add call
        added_target_orm = self.session.add.call_args[0][0]

        # Verify that the persisted object's attribute values match the test object
        self.assertEqual(added_target_orm.name, target_model.name)
        self.assertEqual(added_target_orm.url, target_model.url)


if __name__ == "__main__":
    unittest.main()
