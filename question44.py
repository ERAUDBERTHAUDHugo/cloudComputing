import requests
import json
import time
import calendar
from pprint import pprint
from pymongo import MongoClient
import hashlib
from datetime import datetime

atlas = MongoClient('mongodb+srv://database1:root@cluster0.bj56v.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

db=atlas.dbvelos

lat=input("Entrez lat\n")
lon=input("Entrez lon\n")
dist=input("Entrez distance\n")


def deactivateStation(lat,lon,dist):
	ret=db.stations_states.find({"location": {"$near": {
	        "$geometry":{
	            "type":"Point",
	            "coordinates":[float(lat), float(lon)]},
	        "$maxDistance": float(dist) 
	        },

	    }
	    },)


	for i in ret:
		print(i)
		x=db.stations_states.update_one(i,{"$set":{"status":"Deactivate"}})
		print(x)

# deactivateStation(lat,lon,dist)


def fourty4():

	tt=datetime.timestamp(datetime.now())

	dt_obj= datetime.fromtimestamp(tt)

	print(dt_obj)

	input("ok")

	db.stations_states.aggregate([

		{"$match":{"timestamp":{
		
		}}},
		{"$group":{}}

		])

fourty4()
#50.635014
#3.064802