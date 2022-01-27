import json

from flask import Blueprint

from flask import request
from flask import url_for
from flask import redirect
from flask import session
from flask import jsonify

from .. import redis_client

manage = Blueprint('manage', __name__, url_prefix="/manage")


@manage.route('/test', methods=["POST"])
def test():
    form_data = request.form

    drop_ids = form_data.get("drop_ids").split("\n")
    drop_platform = form_data.get("drop_platform").lower()
    accounts = dict(form_data.lists())["accounts[]"]

    data = {
        "action": "claim",
        "drop_type": "claimdrop",
        "drop_platform": drop_platform,
        "drop_ids": drop_ids,
        # "accounts": [item.split("_")[0] for item in form_data if "account" in item]
        "accounts": accounts
    }

    redis_client.rpush("tasks", json.dumps(data))

    return jsonify({
        "success": True
    })
