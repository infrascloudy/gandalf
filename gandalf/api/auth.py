from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    jwt_required,
    jwt_refresh_token_required,
    create_access_token,
    get_jwt_identity,
    create_refresh_token,
    get_raw_jwt,
)
from sqlalchemy import exc, or_

from gandalf.models.user import User
from gandalf import db, jwt

auth_blueprint = Blueprint("auth", __name__)
blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@auth_blueprint.route("/auth/register", methods=["POST"])
def register_user():
    # get post data
    post_data = request.get_json()
    response_object = {"status": "fail", "message": "Invalid payload."}
    if not post_data:
        return jsonify(response_object), 400
    username = post_data.get("username")
    email = post_data.get("email")
    password = post_data.get("password")
    if not username or not email or not password:
        return response_object, 400
    try:
        # check for existing user
        user = User.query.filter(
            or_(User.username == username, User.email == email)
        ).first()
        if not user:
            # add new user to db
            new_user = User(username=username, email=email)
            new_user.password = password
            db.session.add(new_user)
            db.session.commit()
            # generate auth token
            access_token = create_access_token(identity=username)
            response_object["status"] = "success"
            response_object["message"] = "Successfully registered."
            response_object["access_token"] = access_token
            return jsonify(response_object), 201
        else:
            response_object["message"] = "Sorry. That user already exists."
            return jsonify(response_object), 400
    # handler errors
    except (exc.IntegrityError, ValueError):
        db.session.rollback()
        return jsonify(response_object), 400


@auth_blueprint.route("/auth/login", methods=["POST"])
def login_user():
    # get post data
    post_data = request.get_json()
    response_object = {"status": "fail", "message": "Invalid payload."}
    if not post_data:
        return jsonify(response_object), 400
    email = post_data.get("email")
    password = post_data.get("password")
    try:
        # fetch the user data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password) and user.active:
            access_token = create_access_token(identity=user.username)
            if access_token:
                response_object["status"] = "success"
                response_object["message"] = "Successfully logged in."
                response_object["access_token"] = access_token
                response_object["refresh_token"] = create_refresh_token(
                    identity=user.username
                )
                return jsonify(response_object), 200
        else:
            response_object["message"] = "User does not exist."
            return jsonify(response_object), 404
    except Exception:
        response_object["message"] = "Try again."
        return jsonify(response_object), 500


@auth_blueprint.route("/auth/logout", methods=["GET"])
@jwt_required
def logout_user():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    response_object = {"status": "success", "message": "Successfully logged out."}
    return jsonify(response_object), 200


@auth_blueprint.route("/auth/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    current_user = User.query.filter_by(username=current_user).first()
    ret = {"access_token": create_access_token(identity=current_user)}
    return jsonify(ret), 200


@auth_blueprint.route("/auth/status", methods=["GET"])
@jwt_required
def get_user_status():
    current_user = get_jwt_identity()
    current_user = User.query.filter_by(username=current_user).first()
    # user = User.query.filter_by(id=resp).first()
    response_object = {
        "status": "success",
        "message": "success",
        "data": current_user.to_json(),
    }
    return jsonify(response_object), 200
