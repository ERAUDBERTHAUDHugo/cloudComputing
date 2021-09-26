import requests
import json
import time
import calendar
from pprint import pprint
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient
import hashlib

#CONNEXION TO DB 

atlas = MongoClient('mongodb+srv://database1:root@cluster0.bj56v.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

db=atlas.dbvelos

##GET DATAS FROM APIs

resp=input("Voulez-vous selectionner une ville ?\n (1):Lille (2):Paris (3):Lyon (4):Rennes (Other):Non\n")
lat=input("Entrez votre latitude")
lon=input("Entrez votre longitude")


if resp=="1":
    
    pass
elif resp=="2":
    pass
elif resp == "3":
    pass
elif resp=="4":
    pass
else:
    pass