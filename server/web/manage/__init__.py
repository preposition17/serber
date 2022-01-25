from .manage import manage

from .claimdrop import claimdrop
manage.register_blueprint(claimdrop)