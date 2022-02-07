from flask.blueprints import Blueprint
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for

from .models import db
from .models import Settings as SettingsModel


settings = Blueprint("settings", __name__, url_prefix="/settings")


class Settings:
    def __init__(self):
        settings = SettingsModel.query.all()
        for setting in settings:
            self.__dict__[setting.key] = setting


@settings.route("/")
def settings_view():
    settings = SettingsModel.query.order_by(SettingsModel.id).all()
    return render_template("settings.html", settings=settings)


@settings.route("/set", methods=["POST"])
def set():
    _settings = request.form.to_dict()
    print(_settings)

    for setting_key in _settings.keys():
        if _settings[setting_key] and _settings[setting_key] != "":
            setting = SettingsModel.query.filter_by(key=setting_key).first()
            setting.current = _settings[setting_key]
            db.session.commit()

    return redirect(url_for("settings.settings_view"))

