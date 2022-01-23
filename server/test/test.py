import datetime
from pymongo import MongoClient

client = MongoClient('localhost', 27117)
db = client['admin']
collection = db['finance-book']

