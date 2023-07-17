from flask import request
from flask_restful import Resource
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError
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

    @staticmethod
    def handle_not_found():
        return {"message": "Target not found"}, 404

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
            target_model = self.verify_request(request_json)
            if not target_model:
                return {"message": "Invalid request"}, 400
            self.persist_target(target_model)
            return target_model.dict(), 201
        except IntegrityError as integrity_error:
            self.logger.error(f"Error: {integrity_error}")
            self.session.rollback()
            return {"message": "Target already exists"}, 409
        except Exception as exception:
            return self.handle_error(exception)

    def get(self):
        request_json = request.get_json(force=True)
        self.logger.trace(f"Request json: {request_json}")
        name = request_json.get("name")
        url = request_json.get("url")

        if name:
            target = self.session.query(TargetORM).filter_by(name=name).first()
        elif url:
            target = self.session.query(TargetORM).filter_by(url=url).first()
        else:
            return self.handle_invalid_request()

        if target:
            return TargetModel(name=target.name, url=target.url).dict(), 200
        else:
            return self.handle_not_found()

    def delete(self):
        request_json = request.get_json(force=True)
        self.logger.trace(f"Request json: {request_json}")
        name = request_json.get("name")
        url = request_json.get("url")

        if name:
            target = self.session.query(TargetORM).filter_by(name=name).first()
        elif url:
            target = self.session.query(TargetORM).filter_by(url=url).first()
        else:
            return self.handle_invalid_request()

        if target:
            self.session.delete(target)
            self.session.commit()
            return {"message": "Target deleted"}, 200
        else:
            return self.handle_not_found()

    def update_target(self, target, url):
        target.url = url
        self.session.commit()

    def put(self):
        request_json = request.get_json(force=True)
        self.logger.trace(f"Request json: {request_json}")
        name = request_json.get("name")
        url = request_json.get("url")

        if name and url:
            target = self.session.query(TargetORM).filter_by(name=name).first()
            if target:
                self.update_target(target, url)
                return {"message": "Target updated"}, 200
            else:
                return self.handle_not_found()
        else:
            return self.handle_invalid_request()

    def patch(self):
        request_json = request.get_json(force=True)
        self.logger.trace(f"Request json: {request_json}")
        name = request_json.get("name")
        url = request_json.get("url")

        if name and url:
            target = self.session.query(TargetORM).filter_by(name=name).first()
            if target:
                self.update_target(target, url)
                return {"message": "Target updated"}, 200
            else:
                return self.handle_not_found()
        else:
            return self.handle_invalid_request()
