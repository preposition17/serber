import json
from types import SimpleNamespace

from flask import Blueprint

from flask import request
from flask import url_for
from flask import redirect

from .paths import DATA_FILE


api = Blueprint('api', __name__, url_prefix="/api")


@api.route('/set_keys', methods=["POST"])
def set_keys():

    form = request.form.get("private_keys_placeholder")
    private_keys = form.split("\r\n")

    with open(DATA_FILE, "w+") as data_file:
        print(data_file.read())
        data = json.loads(data_file.read(), object_hook=lambda d: SimpleNamespace(**d))
        print(data["accounts"])

    return redirect(url_for("main.index"))