import requests
import json
import time
import calendar
from pprint import pprint
from pymongo import MongoClient
import hashlib

#CONNEXION TO DB 

atlas = MongoClient('mongodb+srv://database1:root@cluster0.bj56v.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

db=atlas.dbvelos

##GET DATAS FROM APIs

def get_vlille_lille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=3000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

def get_vlille_rennes():
    url="https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel&q=&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json

def get_vlille_paris():
    url_stations_statut="https://velib-metropole-opendata.smoove.pro/opendata/Velib_Metropole/station_status.json"
    url_station_infos="https://velib-metropole-opendata.smoove.pro/opendata/Velib_Metropole/station_information.json"
    response_statut = requests.request("GET", url_stations_statut)
    response_json_statut = json.loads(response_statut.text.encode('utf8'))
    reponse_station=requests.request("GET", url_station_infos)
    response_json_station= json.loads(reponse_station.text.encode('utf8'))
    return  [response_json_statut.get("data", []),response_json_station.get("data", [])]


def get_vlille_lyon():
    url_stations_statut="https://transport.data.gouv.fr/gbfs/lyon/station_status.json"
    url_station_infos="https://transport.data.gouv.fr/gbfs/lyon/station_information.json"
    response_statut = requests.request("GET", url_stations_statut)
    response_json_statut = json.loads(response_statut.text.encode('utf8'))
    reponse_station=requests.request("GET", url_station_infos)
    response_json_station= json.loads(reponse_station.text.encode('utf8'))
    return  [response_json_statut.get("data", []),response_json_station.get("data", [])]



##INSERT DATAS IN DATABASE


#Lille
def insert_station_lille(lille):
    #First, let's clear all station_state collection containing "Lille" as "ville" : 
    x = db["stations_states"].delete_many({"ville":"Lille"})
    for i in lille:
        
        #GET DATA IN THE RIGHT FORMAT
        name=i["fields"]["nom"]
        geoloc=i["fields"]['localisation']
        size=i["fields"]['nbvelosdispo']+i["fields"]['nbplacesdispo']


        available=i["fields"]['etat']

        velo_available=i["fields"]['nbvelosdispo']
        place_available=i["fields"]['nbplacesdispo']

        string_to_encode="Lille"+i["fields"]["nom"]
        string_to_encode=string_to_encode.encode('utf-8')
        unique_id= hashlib.md5()
        unique_id.update(string_to_encode)
        unique_id=str(int(unique_id.hexdigest(), 16))[0:12]
        unique_id=int(unique_id)
        #unique_id=1
    
        timestamp =calendar.timegm(time.gmtime())  

        dataset={"ville" : 'Lille',"name":name,"size":size,"velo_available":velo_available,"place_available":place_available,"geolocalisation":geoloc,"status":available,"size":size,"station_id":unique_id,"timestamp":timestamp}
        
        #INSERT DATA IN HISTORY COLLECTION ADN STATION_STATE COLLECTION
       
        db.stations_states.insert_one(dataset)
        db.history.insert_one(dataset)   

    return 1



#Rennes
def insert_station_rennes(rennes):
    #First, let's clear all station_state collection containing "Rennes" as "ville" : 
    x = db["stations_states"].delete_many({"ville":"Rennes"})

    for i in rennes["records"]:
       
        name=i["fields"]["nom"]
        geoloc=i["fields"]['coordonnees']
        available=i["fields"]['etat']
        size=i["fields"]['nombreemplacementsactuels']
        velo_available=i["fields"]['nombrevelosdisponibles']
        place_available=i["fields"]['nombreemplacementsdisponibles']
        unique_id=i["fields"]['idstation']
        timestamp=calendar.timegm(time.gmtime())  
        dataset={"ville" : 'Rennes',"name":name,"size":size,"velo_available":velo_available,"place_available":place_available,"geolocalisation":geoloc,"status":available,"size":size,"station_id":int(unique_id),"timestamp":timestamp}

        #INSERT DATA IN HISTORY COLLECTION ADN STATION_STATE COLLECTION

        db.stations_states.insert_one(dataset)
        db.history.insert_one(dataset)   


    return 1 

#Paris
def insert_station_paris(paris):

    #First, let's clear all station_state collection containing "Rennes" as "ville" : 
    x = db["stations_states"].delete_many({"ville":"Paris"})

    for i in range(0,len(paris[1]["stations"])):
       
        #print(paris[0]["stations"][i])
        name=paris[1]["stations"][i]["name"]
        geoloc=[paris[1]["stations"][i]["lat"],paris[1]["stations"][i]["lon"]]
        size=paris[0]["stations"][i]['numBikesAvailable']+paris[0]["stations"][i]['num_docks_available']
        
        availablle=paris[0]["stations"][i]["is_installed"]

        available="En Service"
        if availablle!=1:
            available="Pas Disponible"

        velo_available=paris[0]["stations"][i]['numBikesAvailable']
        place_available=paris[0]["stations"][i]['num_docks_available']
        unique_id=paris[0]["stations"][i]['station_id']
        timestamp=calendar.timegm(time.gmtime())  
        
        dataset={"ville" : 'Paris',"name":name,"size":size,"velo_available":velo_available,"place_available":place_available,"geolocalisation":geoloc,"status":available,"size":size,"station_id":unique_id,"timestamp":timestamp}

        #INSERT DATA IN HISTORY COLLECTION ADN STATION_STATE COLLECTION

        db.stations_states.insert_one(dataset)
        db.history.insert_one(dataset)   

    return 1


#Lyon
def insert_station_lyon(lyon):

    #First, let's clear all station_state collection containing "Rennes" as "ville" : 
    x = db["stations_states"].delete_many({"ville":"Lyon"})
    
    for i in range(0,len(lyon[1]["stations"])):
    
        #print(paris[0]["stations"][i])
        name=lyon[1]["stations"][i]["name"]
        geoloc=[lyon[1]["stations"][i]["lat"],lyon[1]["stations"][i]["lon"]]
        size=lyon[0]["stations"][i]['num_bikes_available']+lyon[0]["stations"][i]['num_docks_available']
        velo_available=lyon[0]["stations"][i]['num_bikes_available']
        place_available=lyon[0]["stations"][i]['num_docks_available']
        available=lyon[0]["stations"][i]["is_installed"]
        timestamp=calendar.timegm(time.gmtime())
        unique_id=lyon[1]["stations"][i]["station_id"]
        dataset={"ville" : 'Lyon',"name":name,"size":size,"velo_available":velo_available,"place_available":place_available,"geolocalisation":geoloc,"status":available,"size":size,"station_id":unique_id,"timestamp":timestamp}

        #INSERT DATA IN HISTORY COLLECTION ADN STATION_STATE COLLECTION
        
        db.stations_states.insert_one(dataset)
        db.history.insert_one(dataset)   
    return 1





resp=input("De quelle ville voulez-vous stocker les informations sur les stations de vélos en libre service ? (1) : LILLE | (2) : PARIS | (3) : LYON | (4) : RENNES | (OTHER) : quitter")

while(True):
    if(resp=="1"):
        insert_station_lille(get_vlille_lille())
    elif(resp=="2"):   
        insert_station_paris(get_vlille_paris()) 
    elif(resp=="3"):
        insert_station_lyon(get_vlille_lyon())
    elif(resp=="4"):
        insert_station_rennes(get_vlille_rennes())
    else :
        break
    time.sleep(45)
    