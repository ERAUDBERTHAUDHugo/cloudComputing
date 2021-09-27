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

# lat=input("Entrez lat\n")
# lon=input("Entrez lon\n")
# dist=input("Entrez distance\n")


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


def get_stat():

	# tt=datetime.timestamp(datetime.now())

	# dt_obj= datetime.fromtimestamp(tt)

	# print(dt_obj)

	# input("ok")

	x=db.stations_states.aggregate([

		{"$match":{"timestamp.day":{"$in":[0,1,2,3,4]}}},
		{"$group":{"_id" :{
			"velo_available/place_available" : {
				"$lt" : 0.20}
			}
		}},
		# {"$sort":{"velo_available/place_available":-1}}
		])


	print(x)
	for i in x:
		print(i)

get_stat()
#50.635014
#3.064802