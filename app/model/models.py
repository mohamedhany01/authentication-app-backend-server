from flask import Blueprint
from app import db

app_modules = Blueprint("models", __name__)

# RRM database schema
DEFAULT_STR_LENGTH = 100

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(DEFAULT_STR_LENGTH), nullable=False)
    last_name = db.Column(db.String(DEFAULT_STR_LENGTH), nullable=False)
    email = db.Column(db.String(DEFAULT_STR_LENGTH),
                      unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False)
