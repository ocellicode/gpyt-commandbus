from flask import request
from flask_restful import Resource


class Hello(Resource):
    @staticmethod
    def post():
        json_data = request.get_json(force=True)
        return f"Hello, {json_data['name']}", 201
