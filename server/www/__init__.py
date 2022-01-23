import os

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object('www.config.DevelopConfig')
    app.app_context().push()


    db.init_app(app)
    migrate.init_app(app, db)


    # Login manager
    from .models import User
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))


    # blueprint for utils
    from .utils import utils
    app.register_blueprint(utils)


    # blueprint for main
    from .main import main
    app.register_blueprint(main)

    # blueprint for main
    from .api import api
    app.register_blueprint(api)


    return app
