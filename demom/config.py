import os

from dotenv import load_dotenv


DEBUG = os.getenv("DEBUG") == "1"
MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(MAIN_DIR, ".env")

if DEBUG:
    load_dotenv(ENV_FILE)


class DBConfig:
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")


class RedisConfig:
    REDIS_HOST = os.getenv("REDIS_HOST")


class SocketIoConfig:
    SOCKETIO_HOST = os.getenv("SOCKETIO_HOST")

