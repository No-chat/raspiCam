from sqlite3 import connect
from pymongo import *
from config import config
import datetime

# connect to Mongo Atlas
client = MongoClient(config.mongoURI)
print(datetime.datetime.now())


db = client['CapstoneServer']

print(client.list_database_names())

# disconnect
client.close()