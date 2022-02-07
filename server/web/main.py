from flask import Blueprint
from flask import render_template

from .models import AccountModel

from .settings import Settings


main = Blueprint('main', __name__)


@main.route('/')
def index_view():
    settings = Settings()
    rpc_url = settings.rpc_url.current
    contract_account = settings.contract_account.current
    accounts = AccountModel.query.filter_by(rpc=rpc_url).all()
    return render_template("index.html",
                           rpc_url=rpc_url,
                           contract_account=contract_account,
                           accounts=accounts)


@main.route('/add-accounts')
def add_accounts_view():
    return render_template("add-accounts.html")

