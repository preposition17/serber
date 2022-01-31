import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.automap import automap_base

from sqlalchemy.orm import sessionmaker

from config import DBConfig

db_config = DBConfig()
engine = create_engine(f'postgresql://{db_config.POSTGRES_USER}:'
                       f'{db_config.POSTGRES_PASSWORD}@{db_config.POSTGRES_HOST}/{DBConfig.POSTGRES_DB}')


DeclarativeBase = declarative_base(bind=engine)
AutomapBase = automap_base()
AutomapBase.prepare(engine, reflect=True)
Session = sessionmaker(engine)



class Models:
    WaxAccount = AutomapBase.classes.wax_account
    Settings = AutomapBase.classes.settings


models = Models()
