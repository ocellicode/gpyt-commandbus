import requests
from flask import request
from flask_restful import Resource
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from gpyt_commandbus.model.command import Command as CommandORM
from gpyt_commandbus.model.target import Target as TargetORM

from .model import CommandModel


class Command(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs["logger"]
        self.session: Session = kwargs["session"]

    def post_data_to_endpoint(self, target, data):
        url = (
            self.session.query(TargetORM)
            .filter(TargetORM.name == target)
            .first()
            .url
        )
        response = requests.post(url, json=data, timeout=5)
        response.raise_for_status()

    def verify_request(self, request_json):
        self.logger.trace(f"Request json: {request_json}")
        try:
            return CommandModel(**request_json)
        except ValidationError as validation_error:
            self.logger.error(f"Error: {validation_error}")
            return False

    def persist_command(self, command: CommandModel):
        new_command = CommandORM(**command.dict())
        self.session.add(new_command)
        self.session.commit()
        return new_command

    @staticmethod
    def handle_not_found():
        return {"message": "Command not found"}, 404

    @staticmethod
    def handle_invalid_request():
        return {"message": "Invalid request"}, 400

    def handle_error(self, error):
        self.logger.error(f"Error: {error}")
        return {"message": "Error"}, 500

    def post(self):
        request_json = request.get_json(force=True)
        self.logger.trace(f"Request json: {request_json}")
        try:
            command_model = self.verify_request(request_json)
            if not command_model:
                return {"message": "Invalid request"}, 400
            result = self.persist_command(command_model).get_JSON()
            self.post_data_to_endpoint(result["target_name"], result["data"])
            return result, 201
        except IntegrityError as integrity_error:
            self.logger.error(f"Error: {integrity_error}")
            self.session.rollback()
            return {"message": "Target does not exist"}, 409
        except Exception as exception:  # pylint: disable=broad-except
            return self.handle_error(exception)
