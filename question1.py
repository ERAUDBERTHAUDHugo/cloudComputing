import requests
import json
from pprint import pprint
from pymongo import MongoClient


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

def get_ville_paris():
    url_stations_statut="https://velib-metropole-opendata.smoove.pro/opendata/Velib_Metropole/station_status.json"
    url_station_infos="https://velib-metropole-opendata.smoove.pro/opendata/Velib_Metropole/station_information.json"
    response_statut = requests.request("GET", url_stations_statut)
    response_json_statut = json.loads(response_statut.text.encode('utf8'))
    reponse_station=requests.request("GET", url_station_infos)
    response_json_station= json.loads(reponse_station.text.encode('utf8'))
    return  [response_json_statut.get("data", []),response_json_station.get("data", [])]


def get_ville_lyon():
    url_stations_statut="https://transport.data.gouv.fr/gbfs/lyon/station_status.json"
    url_station_infos="https://transport.data.gouv.fr/gbfs/lyon/station_information.json"
    response_statut = requests.request("GET", url_stations_statut)
    response_json_statut = json.loads(response_statut.text.encode('utf8'))
    reponse_station=requests.request("GET", url_station_infos)
    response_json_station= json.loads(reponse_station.text.encode('utf8'))
    return  [response_json_statut.get("data", []),response_json_station.get("data", [])]

lille = get_vlille_lille()
paris = get_ville_paris()
rennes = get_vlille_rennes()
lyon = get_ville_lyon()


#Lille
def show_data_station_lille(lille):
    print("LES STATIONS DE VELOS EN LIBRE SERVICE DE LILLE SONT :")
    for i in lille:
        
        name=i["fields"]["nom"]
        geoloc=i["fields"]['localisation']
        size=i["fields"]['nbvelosdispo']+i["fields"]['nbplacesdispo']

        if(i["fields"]['type'][0]=="A"):
            tpe=True
        else :
            tpe=False

        available=i["fields"]['etat']
    
        dataset={"geolocalisation":geoloc,"size":size,"name":name,"tpe":tpe,"available":available}
        print(dataset)
    return 1



def show_data_station_rennes(rennes):
    #print(rennes)
    print("LES STATIONS DE VELOS EN LIBRE SERVICE DE RENNES SONT : ")
    for i in rennes["records"]:
        #print(i["fields"])
       
        name=i["fields"]["nom"]
        geoloc=i["fields"]['coordonnees']
        tpe=""
        available=i["fields"]['etat']
        size=i["fields"]['nombreemplacementsactuels']
        dataset={"geolocalisation":geoloc,"size":size,"name":name,"tpe":tpe,"available":available}
        print(dataset)
    return 1



def show_data_station_paris(paris):
 
    print("LES STATIONS DE VELOS EN LIBRE SERVICE DE PARIS SONT : ")
    
    for i in range(0,len(paris[1]["stations"])):
       
        #print(paris[0]["stations"][i])
        name=paris[1]["stations"][i]["name"]
        geoloc=[paris[1]["stations"][i]["lat"],paris[1]["stations"][i]["lon"]]
        size=paris[1]["stations"][i]['capacity']
        tpe=""
        available=paris[0]["stations"][i]["is_installed"]
        dataset={"geolocalisation":geoloc,"size":size,"name":name,"tpe":tpe,"available":available}
        print(dataset)
    return 1

def show_data_station_lyon(lyon):
 
    print("LES STATIONS DE VELOS EN LIBRE SERVICE DE LYON SONT : ")
    
    for i in range(0,len(lyon[1]["stations"])):
    
        #print(paris[0]["stations"][i])
        name=lyon[1]["stations"][i]["name"]
        geoloc=[lyon[1]["stations"][i]["lat"],lyon[1]["stations"][i]["lon"]]
        size=lyon[0]["stations"][i]['num_bikes_available']+lyon[0]["stations"][i]['num_docks_available']
        tpe=""
        available=lyon[0]["stations"][i]["is_installed"]
        dataset={"geolocalisation":geoloc,"size":size,"name":name,"tpe":tpe,"available":available}
        print(dataset)
    return 1



while(True):
    resp=input("De quelle ville voulez-vous voir les informations sur les stations de vélos en libre service ? (1) : LILLE | (2) : PARIS | (3) : LYON | (4) : RENNES | (OTHER) : quitter")

    if(resp=="1"):
        show_data_station_lille(lille)
    elif(resp=="2"):   
        show_data_station_paris(paris) 
    elif(resp=="3"):
        show_data_station_lyon(lyon)
    elif(resp=="4"):
        show_data_station_rennes(rennes)
    else :
        break



