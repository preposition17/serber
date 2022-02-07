import time
import threading

from eospy.cleos import Cleos
from api.api import Api

from drop import NeftyDrop, AtomicDrop

from account import Account, Accounts


def claim_drop(settings, drop_ids, accounts_keys, sio):
    # SETTINGS
    contract_account = settings.contract_account
    rpc_url = settings.rpc_url
    claim_time = int(settings.claim_time)

    cleos = Cleos(url=rpc_url)
    api = Api(url=rpc_url)

    sio.emit("debug_script", "* Claimdrop task received")
    if contract_account == "neftyblocksd":
        drops = [NeftyDrop(cleos, drop_id) for drop_id in drop_ids]
    elif contract_account == "atomicdropsx":
        drops = [AtomicDrop(cleos, drop_id) for drop_id in drop_ids]
    else:
        sio.emit("debug_script", "! Error while drops initializing")
        return

    sio.emit("debug_script", "* Drops initialized")
    accounts = Accounts([Account(api, cleos, key) for key in accounts_keys])
    sio.emit("debug_script", "* Accounts initialized")

    # for drop in drops:
    #     accounts.deposit_all(drop, True, sio)

    sio.emit("debug_script", "* Accounts deposited")

    def claim(drop):
        if drop.start_time > time.time():
            print("The drop has not started yet, waiting...")
            sio.emit("debug_script", "* The drop has not started yet, waiting...")

        while drop.start_time - time.time() < claim_time:
            continue

        accounts.claim_all(drop)

    for drop in drops:
        claim_thread = threading.Thread(target=claim, args=(drop,))
        claim_thread.start()