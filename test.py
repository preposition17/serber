import json
import time

from eospy.cleos import Cleos
from eospy.keys import EOSKey

from api.api import Api

from account import Account, Accounts
from drop import AtomicDrop, NeftyDrop

url = "https://testnet.waxsweden.org"
contract_account = "neftyblocksd"
drop_id = 1019

ce = Cleos(url=url)
api = Api(url=url)

accounts = Account.load_accounts(api, ce, "private_keys.json")
accounts = Accounts(accounts)

drop = NeftyDrop(ce, 1033)
drop.print_info()

accounts.set_assets_all()
for account in accounts.accounts:
    print(account.assets)


accounts.deposit_all(drop)

if drop.start_time > time.time():
    print("The drop has not started yet, waiting...")


while drop.start_time - time.time() > 0:
    continue


accounts.claim_with_assets_all(drop)










