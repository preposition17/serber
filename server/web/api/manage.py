import json

from flask import Blueprint

from flask import request
from flask import url_for
from flask import redirect
from flask import session

from .. import redis_client

manage = Blueprint('manage', __name__, url_prefix="/manage")


@manage.route('/test', methods=["POST"])
def test():
    form_data = request.form
    drop_ids = form_data.get("drop_ids_textarea")

    data = {
        "drop_type": "claimdrop",
        "drop_ids": drop_ids,
        "accounts": [item.split("_")[0] for item in form_data if "account" in item]
    }
    redis_client.rpush("tasks", json.dumps(data))

    return redirect(session["last_url"])
