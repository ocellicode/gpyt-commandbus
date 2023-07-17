import unittest
from unittest.mock import MagicMock

from flask import Flask
from flask_restful import Api
from loguru import logger
from sqlalchemy.exc import IntegrityError
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

    def test_post_target_duplicate(self):
        target_data = {"name": "example", "url": "http://example.com"}
        self.session.add.side_effect = IntegrityError("Test error", None, None)
        response = self.client.post("/target", json=target_data)
        self.assertEqual(response.status_code, 409)

        # Verify that the error message is returned
        response_data = response.get_json()
        self.assertEqual(response_data, {"message": "Target already exists"})

        # Verify that the session methods were called
        self.session.add.assert_called_once()
        self.session.commit.assert_not_called()

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

    def test_post_target(self):
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

    def test_get_target_name(self):
        the_dict = {"name": "example", "url": "http://example.com"}
        target_orm = TargetORM(**the_dict)
        self.session.query.return_value.filter_by.return_value.first.return_value = (
            target_orm
        )

        response = self.client.get("/target", json={"name": the_dict["name"]})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), the_dict)

    def test_get_target_url(self):
        the_dict = {"name": "example", "url": "http://example.com"}
        target_orm = TargetORM(**the_dict)
        self.session.query.return_value.filter_by.return_value.first.return_value = (
            target_orm
        )

        response = self.client.get("/target", json={"url": the_dict["url"]})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), the_dict)

    def test_get_target_name_not_found(self):
        response_dict = {"message": "Target not found"}

        self.session.query.return_value.filter_by.return_value.first.return_value = None

        response = self.client.get("/target", json={"name": "broken"})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), response_dict)

    def test_get_target_url_not_found(self):
        response_dict = {"message": "Target not found"}

        self.session.query.return_value.filter_by.return_value.first.return_value = None

        response = self.client.get("/target", json={"url": "https://foo.com"})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), response_dict)

    def test_target_get_invalid_request(self):
        response_dict = {"message": "Invalid request"}

        response = self.client.get("/target", json={"invalid": "request"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), response_dict)

    def test_target_put(self):
        the_dict = {"name": "example", "url": "http://example.com"}
        target_orm = TargetORM(**the_dict)
        self.session.query.return_value.filter_by.return_value.first.return_value = (
            target_orm
        )

        response = self.client.put("/target", json=the_dict)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Target updated"})

    def test_target_put_not_found(self):
        response_dict = {"message": "Target not found"}

        self.session.query.return_value.filter_by.return_value.first.return_value = None

        response = self.client.put("/target", json={"name": "broken", "url": "broken"})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), response_dict)

    def test_target_put_invalid_request(self):
        response_dict = {"message": "Invalid request"}

        response = self.client.put("/target", json={"invalid": "request"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), response_dict)

    def test_target_delete_by_name(self):
        the_dict = {"name": "example", "url": "http://example.com"}
        target_orm = TargetORM(**the_dict)
        self.session.query.return_value.filter_by.return_value.first.return_value = (
            target_orm
        )

        response = self.client.delete("/target", json=the_dict)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Target deleted"})

    def test_target_delete_by_url(self):
        the_dict = {"name": "example", "url": "http://example.com"}
        target_orm = TargetORM(**the_dict)
        self.session.query.return_value.filter_by.return_value.first.return_value = (
            target_orm
        )

        response = self.client.delete("/target", json={"url": the_dict["url"]})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Target deleted"})

    def test_target_delete_by_name_not_found(self):
        response_dict = {"message": "Target not found"}

        self.session.query.return_value.filter_by.return_value.first.return_value = None

        response = self.client.delete("/target", json={"name": "broken"})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), response_dict)

    def test_target_delete_by_url_not_found(self):
        response_dict = {"message": "Target not found"}

        self.session.query.return_value.filter_by.return_value.first.return_value = None

        response = self.client.delete("/target", json={"url": "broken"})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), response_dict)

    def test_target_delete_invalid_request(self):
        response_dict = {"message": "Invalid request"}

        response = self.client.delete("/target", json={"invalid": "request"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), response_dict)

    def test_target_patch(self):
        the_dict = {"name": "example", "url": "http://example.com"}
        target_orm = TargetORM(**the_dict)
        self.session.query.return_value.filter_by.return_value.first.return_value = (
            target_orm
        )

        response = self.client.patch("/target", json=the_dict)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Target updated"})

    def test_target_patch_not_found(self):
        response_dict = {"message": "Target not found"}

        self.session.query.return_value.filter_by.return_value.first.return_value = None

        response = self.client.patch(
            "/target", json={"name": "broken", "url": "broken"}
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), response_dict)

    def test_target_patch_invalid_request(self):
        response_dict = {"message": "Invalid request"}

        response = self.client.patch("/target", json={"invalid": "request"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), response_dict)
