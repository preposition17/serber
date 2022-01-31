from datetime import datetime

from flask_login import UserMixin

from . import db


class UserModel(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)


class AccountModel(db.Model):
    __tablename__ = "wax_account"

    id = db.Column(db.Integer, primary_key=True)
    private_token = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(12), nullable=False, unique=True)
    atomic_drop_balance = db.Column(db.Float)
    nefty_drop_balance = db.Column(db.Float)
    balance = db.Column(db.Float)
    cpu = db.Column(db.Float)
    ram = db.Column(db.Float)
    update_time = db.Column(db.DateTime, default=datetime.now())

    # disabled = False



class Settings(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    key = db.Column(db.String, nullable=False, unique=True)
    current = db.Column(db.String, nullable=False)
    value = db.Column(db.String)
    is_input = db.Column(db.Boolean, default=True)
    is_select = db.Column(db.Boolean, default=False)
    is_check = db.Column(db.Boolean, default=False)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


# db.create_all(app=current_app)