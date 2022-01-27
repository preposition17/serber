import os
import time
import json
import threading

from dotenv import load_dotenv

import redis
import websocket

from eospy.cleos import Cleos
from eospy.keys import EOSKey

from api.api import Api

from account import Account, Accounts
from drop import AtomicDrop, NeftyDrop


if os.getenv("DEBUG") == "1":
    load_dotenv()


redis_client = redis.Redis(host=os.getenv("REDIS_HOST"))
if not redis_client.ping():
    print("Redis not responding")
    exit()


def on_message(wsapp, message):
    print(message)


ws = websocket.WebSocketApp("ws://127.0.0.1:5000/test", on_message=on_message)





def main_worker():
    time.sleep(2)
    ws.send(json.dumps({
        "message": "* DEMOM started"
    }))
    print("* DEMOM started")
    while True:
        ws.send(json.dumps({
            "message": "* PING"
        }))

        command = redis_client.lpop("tasks")
        if command:
            print(command.decode("UTF-8"))

        time.sleep(1)


if __name__ == '__main__':
    main_worker_thread = threading.Thread(target=main_worker)
    main_worker_thread.start()
    ws.run_forever()

