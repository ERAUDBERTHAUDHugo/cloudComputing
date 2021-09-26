import requests
import json
import time
from pprint import pprint
from pymongo import MongoClient

atlas = MongoClient('mongodb+srv://database1:root@cluster0.bj56v.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

db=atlas.dbvelos

x = db["history"].delete_many({"ville":"Paris"})

