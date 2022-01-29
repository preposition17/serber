import os
import time
import json
import threading

from dotenv import load_dotenv

import redis
import socketio

from eospy.cleos import Cleos

from api.api import Api

from account import Account, Accounts
from drop import AtomicDrop, NeftyDrop


if os.getenv("DEBUG") == "1":
    load_dotenv()


url = "https://testnet.waxsweden.org"
ce = Cleos(url=url)
api = Api(url=url)


redis_client = redis.Redis(host=os.getenv("REDIS_HOST"))
if not redis_client.ping():
    print("Redis not responding")
    exit()


sio = socketio.Client()


def claim_drop(drop_platform, drop_ids, accounts_keys):
    sio.emit("debug_script", "* Claimdrop task received")
    if drop_platform == "neftyblocks":
        drops = [NeftyDrop(ce, drop_id) for drop_id in drop_ids]
    elif drop_platform == "atomichub":
        drops = [AtomicDrop(ce, drop_id) for drop_id in drop_ids]
    else:
        sio.emit("debug_script", "! Error while drops initializing")
        return

    sio.emit("debug_script", "* Drops initialized")
    accounts = Accounts([Account(api, ce, key) for key in accounts_keys])
    sio.emit("debug_script", "* Accounts initialized")

    for drop in drops:
        accounts.deposit_all(drop, True, sio)

    sio.emit("debug_script", "* Accounts deposited")

    def claim(drop):
        if drop.start_time > time.time():
            print("The drop has not started yet, waiting...")
            sio.emit("debug_script", "* The drop has not started yet, waiting...")

        while drop.start_time - time.time() > 0:
            continue

        accounts.claim_all(drop)

    for drop in drops:
        claim_thread = threading.Thread(target=claim, args=(drop,))
        claim_thread.start()



def main_worker():
    time.sleep(2)

    print("* DEMOM started")
    sio.emit("debug_script", "* DEMOM started")
    while True:


        command = redis_client.lpop("tasks")
        if command:
            command = json.loads(command.decode("UTF-8"))
            print(command)
            if command["action"] == "claim":
                claim_thread = threading.Thread(target=claim_drop,
                                                args=(command["drop_platform"],
                                                      command["drop_ids"],
                                                      command["accounts"]))
                claim_thread.start()

        time.sleep(1)


if __name__ == '__main__':
    sio.connect('http://127.0.0.1:5000/')

    main_worker_thread = threading.Thread(target=main_worker)
    main_worker_thread.start()

    sio.wait()

