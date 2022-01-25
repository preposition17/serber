import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:


    # Main configs
    DEBUG = False
    CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Database configs
    DATABASE_FILE = os.getenv('DATABASE_FILE')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_FILE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File upload configs
    UPLOAD_FOLDER = ['static', 'img']
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


class ProductionConfig(Config):
    DEBUG = False


class DevelopConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True