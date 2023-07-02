from flask import request
from flask_restful import Resource


class Hello(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs["logger"]

    def post(self):
        json_data = request.get_json(force=True)
        self.logger.trace(f"Hello, {json_data['name']}")
        return f"Hello, {json_data['name']}", 201
