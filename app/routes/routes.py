from json import dumps
import sqlite3
from flask import Blueprint, request, abort, Response
import sqlalchemy
from app.model.models import User
from app import bcrypt, db
from datetime import datetime
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

app_routes = Blueprint("routes", __name__)


@app_routes.route("/hello")
def hello():

    return {
        "testing": True,
        "message": Hello, world
    }

@app_routes.route("/")
@jwt_required()
def protected():

    authenticated_user = get_jwt_identity()
    return {
        "authenticated": True,
        "user_data": authenticated_user
    }, 200


@app_routes.route("/register", methods=["POST"])
def register():

    json_request = request.get_json()
    firstName = json_request["firstName"]
    lastName = json_request["lastName"]
    email = json_request["email"]
    password = json_request["password"]
    today_date = datetime.now()

    # Is user exist
    user = User.query.filter((User.email == email)).first()

    if(user):
        return {"authenticated": False, "message": "This user is exist", "registered": True}

    # Hashing the password
    hashed_password = bcrypt.generate_password_hash(
        password).decode("utf-8")

    # Save data in db
    new_user = User(first_name=firstName, last_name=lastName, email=email,
                    password=hashed_password, last_login=today_date, registration_date=today_date)
    db.session.add(new_user)

    message_on_commit_failure = {"authenticated": False,
                                 "message": "Error in commiting data", "registered": False}
    try:
        db.session.commit()

        new_user = User.query.filter((User.email == email)).first()
        access_token = create_access_token(
            identity=dumps({"id": new_user.id, "first_name": new_user.first_name, "last_name": new_user.last_name, "email": new_user.email}))

        return ({
            "authenticated": True,
            "jwt_token": access_token
        })

    except AssertionError as err:
        db.session.rollback()
        abort(Response(dumps(message_on_commit_failure), 409))
    except (sqlalchemy.exc.IntegrityError, sqlite3.IntegrityError) as err:
        db.session.rollback()
        abort(Response(dumps(message_on_commit_failure), 409))
    except Exception as err:
        db.session.rollback()
        abort(Response(dumps(message_on_commit_failure), 500))
    finally:
        db.session.close()


@app_routes.route("/login", methods=["POST"])
def login():

    json_request = request.get_json()
    email = json_request["email"]
    password = json_request["password"]

    # Is user exist
    user = User.query.filter((User.email == email)).first()

    if(not user):
        return {"authenticated": False, "message": "This user isn't exist", "error": True}

    # Check passwords
    db_password = user.password

    are_matched = bcrypt.check_password_hash(db_password, password)

    if(not are_matched):
        return {"authenticated": False, "message": "Bad email or password"}, 401

    access_token = create_access_token(
        identity=dumps({"id": user.id, "first_name": user.first_name, "last_name": user.last_name, "email": user.email}))

    return ({
            "authenticated": True,
            "jwt_token": access_token
            }, 200)
