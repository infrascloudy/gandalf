from flask import Blueprint
from flask_restful import Resource, Api


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")
api = Api(auth_blueprint)


class AuthPing(Resource):
    def get(self):
        return {"status": "success", "message": "pong!"}


api.add_resource(AuthPing, "/ping")
