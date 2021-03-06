import json

from flask import Blueprint

from flask import request
from flask import url_for
from flask import redirect
from flask import jsonify

from eospy.cleos import Cleos
from api.api import Api
from .. import redis_client

from account import Account, Accounts

from ..models import db
from ..models import AccountModel

from ..settings import Settings


api = Blueprint('api', __name__, url_prefix="/api")


@api.route('/set_keys', methods=["POST"])
def set_keys():
    settings = Settings()

    # TODO: Register from demom
    ce = Cleos(url=settings.rpc_url.current)
    wax_api = Api(url=settings.rpc_url.current)

    form = request.form.get("private_keys_placeholder")
    private_keys = form.split("\r\n")

    for private_key in private_keys:
        account = Account(wax_api, ce, private_key)
        account = AccountModel(private_token=private_key, name=account.name, rpc=settings.rpc_url.current)
        db.session.add(account)
    db.session.commit()

    return redirect(url_for("main.index_view"))


@api.route('/update_accs_info', methods=["POST"])
def update_accs_info():

    # accounts = AccountModel.query.all()
    data = {
        "action": "update_accounts_data"
    }
    redis_client.rpush("tasks", json.dumps(data))

    return jsonify({"success": True})