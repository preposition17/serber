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
    return render_template("index.html",
                           contract_account=contract_account,
                           accounts=accounts)


@main.route('/add-accounts')
def add_accounts_view():
    return render_template("add-accounts.html")

