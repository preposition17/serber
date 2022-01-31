import os
import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

load_dotenv("docker.env")
user_name = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
my_db = os.getenv("POSTGRES_DB")

engine = create_engine(f"postgresql://{user_name}:{password}@localhost/{my_db}")
engine.connect()

DeclarativeBase = declarative_base()
AutomapBase = automap_base()
Session = sessionmaker(bind=engine)

AutomapBase.prepare(engine, reflect=True)
Accounts = AutomapBase.classes.wax_account

with Session() as session:
    user = session.query(Accounts).first()
    print(user.private_token)
