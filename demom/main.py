import os
import time
import json

from dotenv import load_dotenv

import redis

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


while True:
    pass

