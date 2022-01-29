from flask import Blueprint
from flask import render_template
from flask import current_app

from .models import AccountModel
from .models import Settings

from . import api
from . import ce
from . import contract_account      # TODO: change to import from db

from account import Account


main = Blueprint('main', __name__)


@main.route('/')
def index_view():
    accounts = AccountModel.query.all()

    accounts_list = list()
    for account in accounts:
        account = Account(api, ce, account.private_token)
        accounts_list.append(account)

    return render_template("index.html",
                           contract_account=contract_account,
                           accounts=accounts_list)


@main.route('/add-accounts')
def add_accounts_view():
    return render_template("add-accounts.html")


@main.route('/settings')
def settings_view():
    settings = Settings.query.all()
    print(settings)
    return render_template("settings.html", settings=settings)

