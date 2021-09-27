import requests
import json
import time
from pprint import pprint
from pymongo import MongoClient
from datetime import datetime




timestamp = 1632686488
dt_obj = datetime.fromtimestamp(timestamp)
print(dt_obj.hour)
print(dt_obj.weekday())