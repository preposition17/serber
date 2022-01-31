import os
import time
import json
import threading


import socketio


from eospy.cleos import Cleos

from api.api import Api

from account import Account, Accounts
from drop import AtomicDrop, NeftyDrop

from tasks import update_accounts_data
from tasks import claim_drop


from redis_client import get_redis_client

from settings import Settings
import config


settings = Settings()

redis_client = get_redis_client()
sio = socketio.Client()
sio_config = config.SocketIoConfig()


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
                                                args=(settings,
                                                      command["drop_ids"],
                                                      command["accounts"],
                                                      sio))
                claim_thread.start()
            if command["action"] == "update_accounts_data":
                accounts_data_updating_thread = threading.Thread(target=update_accounts_data,
                                                                 args=(settings,))
                accounts_data_updating_thread.start()


        time.sleep(1)


if __name__ == '__main__':
    sio.connect(sio_config.SOCKETIO_HOST)

    main_worker_thread = threading.Thread(target=main_worker)
    main_worker_thread.start()

    settings.updater_start()

    sio.wait()

