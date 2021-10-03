from pprint import pprint
from pymongo import MongoClient


#CONNEXION TO DB 

atlas = MongoClient('mongodb+srv://database1:root@cluster0.bj56v.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

db=atlas.dbvelos

##GET DATAS FROM APIs

resp=input("Voulez-vous selectionner une ville ?\n (1):Lille (2):Paris (3):Lyon (4):Rennes (Other):Non\n")
lat=input("Entrez votre latitude")
lon=input("Entrez votre longitude")
nbreStation=input("combien de stations voulez-vous afficher ?")


if resp=="1":
    ret=db.stations_states.find({"ville":"Lille","location": {"$near": {
        "$geometry":{
            "type":"Point",
            "coordinates":[float(lat), float(lon)]},
       
        }
    }},
    {"_id":0,"timestamp":0,"size":0}
    ).limit(int(nbreStation))
    for i in ret:
        pprint(i)
elif resp=="2":
    ret=db.stations_states.find({"ville":"Paris","location": {"$near": {
        "$geometry":{
            "type":"Point",
            "coordinates":[float(lat), float(lon)]},
       
        }
    }},
    {"_id":0,"timestamp":0,"size":0}
    ).limit(int(nbreStation))
    for i in ret:
        pprint(i)
    
elif resp == "3":
    ret=db.stations_states.find({ "ville":"Lyon","location": {"$near": {
        "$geometry":{
            "type":"Point",
            "coordinates":[float(lat), float(lon)]},
       
        }
    }},
    {"_id":0,"timestamp":0,"size":0}
    ).limit(int(nbreStation))
    for i in ret:
        pprint(i)

elif resp=="4":
    ret=db.stations_states.find({"ville":"Rennes","location": {"$near": {
        "$geometry":{
            "type":"Point",
            "coordinates":[float(lat), float(lon)]},
       
        }
    }},
    {"_id":0,"timestamp":0,"size":0}
    ).limit(int(nbreStation))
    for i in ret:
        pprint(i)
else:
    ret=db.stations_states.find({"location": {"$near": {
        "$geometry":{
            "type":"Point",
            "coordinates":[float(lat), float(lon)]},
       
        }
    }},
    {"_id":0,"timestamp":0,"size":0}
    ).limit(int(nbreStation))
    for i in ret:
        print(i)
    