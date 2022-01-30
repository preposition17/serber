from datetime import datetime

from models import Session
from models import models

from account import Account


def update_accounts_data(api, cleos):
    with Session() as db_session:
        accounts = db_session.query(models.WaxAccount).all()
        for account in accounts:
            account_inst = Account(api, cleos, account.private_token)
            account_data = account_inst.full_data
            account.balance = account_data["tokens"][0]["amount"] if account_data["tokens"] else 0
            account.atomic_drop_balance = account_data["atomic_drop_balance"]
            account.nefty_drop_balance = account_data["nefty_drop_balance"]
            account.cpu = account_data["account"]["cpu_limit"]["used"]/account_data["account"]["cpu_limit"]["max"] * 100
            account.net = account_data["account"]["net_limit"]["used"]/account_data["account"]["net_limit"]["max"] * 100
            account.ram = account_data["account"]["ram_usage"] / account_data["account"]["ram_quota"] * 100
            account.update_time = datetime.utcnow()
            db_session.commit()
