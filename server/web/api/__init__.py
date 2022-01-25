from .api import api


from .manage import manage
api.register_blueprint(manage)