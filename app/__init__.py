from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)

""" App Variables """
ONE_HOUR = 1 * 60 * 60
DATABASE_URI = f"{getenv('DATABASE_VENDOR')}://{getenv('DATABASE_USER')}:{getenv('DATABASE_PASSWORD')}@{getenv('DATABASE_URL')}/{getenv('DATABASE_NAME')}"
APP_SECRET = getenv("SECRET")

"""App configrations"""
app.config["SECRET_KEY"] = APP_SECRET
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = APP_SECRET
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ONE_HOUR

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# App Blueprints
from app.routes.routes import app_routes
from app.model.models import app_modules

app.register_blueprint(app_routes)
app.register_blueprint(app_modules)
