from flask import request
from flask_restful import Resource
from pydantic.error_wrappers import ValidationError
from sqlalchemy.orm import Session

from gpyt_commandbus.model.target import Target as TargetORM

from .targetmodel import TargetModel


class Target(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs["logger"]
        self.session: Session = kwargs["session"]

    def verify_request(self, request_json):
        self.logger.trace(f"Request json: {request_json}")
        try:
            return TargetModel(**request_json)
        except ValidationError as validation_error:
            self.logger.error(f"Error: {validation_error}")
            return False

    def persist_target(self, target: TargetModel):
        new_target = TargetORM(**target.dict())
        self.session.add(new_target)
        self.session.commit()

    def post(self):
        request_json = request.get_json(force=True)
        self.logger.trace(f"Request json: {request_json}")
        try:
            target_model = self.verify_request(request_json)
            if not target_model:
                return {"message": "Invalid request"}, 400
            self.persist_target(target_model)
            return target_model.dict(), 201
        except Exception as odd_exception:  # pylint: disable=broad-except
            self.logger.error(f"Error: {odd_exception}")
            return {"message": "Error"}, 500
