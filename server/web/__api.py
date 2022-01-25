import json
from types import SimpleNamespace

from flask import Blueprint

from flask import request
from flask import url_for
from flask import redirect


from .models import db
from .models import AccountModel


api = Blueprint('api', __name__, url_prefix="/api")


@api.route('/set_keys', methods=["POST"])
def set_keys():

    form = request.form.get("private_keys_placeholder")
    private_keys = form.split("\r\n")

    for private_key in private_keys:
        account = AccountModel(private_token=private_key)
        db.session.add(account)
    db.session.commit()

    return redirect(url_for("main.index_view"))