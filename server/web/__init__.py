from flask import Flask
from flask_socketio import SocketIO
from flask_jsglue import JSGlue

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from eospy.cleos import Cleos
from api.api import Api
import redis

from .utils import check_db_file
from .jinja_utils import cstm_context_processor


db = SQLAlchemy()
migrate = Migrate()

url = "https://testnet.waxsweden.org"
contract_account = "neftyblocksd"

ce = Cleos(url=url)
api = Api(url=url)
redis_client = redis.Redis()


def create_app():
    app = Flask(__name__)
    app.config.from_object('web.config.DevelopConfig')
    app.app_context().push()

    db.init_app(app)
    migrate.init_app(app, db)

    socketio = SocketIO()
    socketio.init_app(app)

    jsglue = JSGlue()
    jsglue.init_app(app)

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

    # blueprint for main
    from .settings import settings
    app.register_blueprint(settings)

    # blueprint for manage
    from .manage import manage
    app.register_blueprint(manage)

    # blueprint for main
    from .api import api
    app.register_blueprint(api)

    # blueprint for websocket
    from .manage import script_ws
    app.register_blueprint(script_ws)

    @app.context_processor
    def context_processor():
        return cstm_context_processor()

    return app



