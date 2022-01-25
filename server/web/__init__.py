from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from .utils import check_db_file
from .utils import set_all_urls


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object('web.config.DevelopConfig')
    app.app_context().push()

    db.init_app(app)
    migrate.init_app(app, db)

    # Login manager
    from .models import UserModel
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return UserModel.query.get(int(user_id))

    # blueprint for utils
    from .utils import utils
    app.register_blueprint(utils)


    # blueprint for main
    from .main import main
    app.register_blueprint(main)

    # blueprint for manage
    from .manage import manage
    app.register_blueprint(manage)

    # blueprint for main
    from .api import api
    app.register_blueprint(api)

    # set_all_urls(app)

    return app
