from flask import Blueprint
from flask import render_template

from .models import AccountModel
from .models import Settings
from .models import UrlModel


from eospy.cleos import Cleos
from eospy.keys import EOSKey

from api.api import Api

from account import Account, Accounts
from drop import AtomicDrop, NeftyDrop

url = "https://testnet.waxsweden.org"
contract_account = "neftyblocksd"

ce = Cleos(url=url)
api = Api(url=url)


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


@main.route('/settings')
def settings_view():
    settings = Settings.query.all()
    print(settings)
    return render_template("settings.html", settings=settings)


@main.route('/manage')
def manage_view():
    return render_template("manage.html")