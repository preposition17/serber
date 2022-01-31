from flask import Blueprint

from flask import request
from flask import url_for
from flask import render_template
from flask import current_app
from flask import session


from ..settings import Settings

from ..models import AccountModel

claimdrop = Blueprint('claimdrop', __name__)


@claimdrop.route("/claimdrop")
def claimdrop_view():
    session["last_url"] = url_for("manage.claimdrop.claimdrop_view")
    accounts = AccountModel.query.all()
    settings = Settings()

    return render_template("manage/claimdrop.html",
                           accounts=accounts,
                           current_contract = settings.contract_account.current
                           )