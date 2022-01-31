import time
import traceback

import redis

import config


def get_redis_client():

    redis_config = config.RedisConfig()
    redis_client = redis.Redis(host=redis_config.REDIS_HOST, client_name="Demom")


    try_num = 1
    while True:
        try:
            if redis_client.ping():
                return redis_client
            else:
                print(f"* GET_REDIS_CLIENT: Error while connection to redis... Tries: {try_num}")
                try_num += 1
        except Exception as ex:
            print(f"* GET_REDIS_CLIENT: Error while connection to redis... Tries: {try_num}")
            if config.DEBUG:
                traceback.print_tb(ex.__traceback__)

            if try_num > 30:
                print(f"* GET_REDIS_CLIENT: Exiting...")
                exit()

            try_num += 1
            time.sleep(1)