import os

from flask import current_app
from flask import url_for

from flask_login import UserMixin
from sqlalchemy.exc import IntegrityError

from . import db

from .utils import check_db_file


class UserModel(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)


class AccountModel(db.Model):
    __tablename__ = "wax_account"

    id = db.Column(db.Integer, primary_key=True)
    private_token = db.Column(db.String(30), nullable=False, unique=True)

    # disabled = False



class Settings(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String, nullable=False, unique=True)
    default = db.Column(db.String, nullable=False)
    value = db.Column(db.String)


class UrlModel(db.Model):
    __tablename__ = "url"

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, unique=True)
    is_main = db.Column(db.Boolean, default=True)
    is_visible = db.Column(db.Boolean, default=True)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


check_db_file(current_app, db, os.getenv("DATABASE_FILE"))


settings = {
    "api_url": "https://testnet.waxsweden.org",
    "contract_account": "neftyblocksd"
}

for key in settings.keys():
    setting = Settings(key=key, default=settings[key])
    db.session.add(setting)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()