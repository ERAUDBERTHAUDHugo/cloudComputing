from pprint import pprint
from pymongo import MongoClient


atlas = MongoClient('mongodb+srv://database1:root@cluster0.bj56v.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')

db=atlas.dbvelos


def get_station_by_input(ville,search_string):
	found=db.stations_states.find(({"ville":ville, "name": { "$regex": search_string.upper() } }))
	for i in found:
		pprint(i)
	return found

def update_or_delete_station(ville):
	
	cond=True
	while cond:
		station=input("Quelle station voulez vous mettre à jour ou supprimer ?")
		result=get_station_by_input(ville,station)
		size=len(list(result.clone()))
		station_to_modify=result.clone()
		for i in result:
			pprint(i)
		if(size==1):
			confirmation=input("Est-ce bien la station que vous voulez modifer ou supprimer ? (1) : OUI | (2) : NON ")
			if(confirmation=="1"):
				cond=False
				break
		else:
			print("Vous ne pouvez pas faire de modification ou de suppression sur plus d'une station à la fois. Veuillez réitérer votre recherche.")
	
	station_action=input("Voulez-vous : (1) : Supprimer la station | (2) : Modifier la station | (3) : Quitter ")    

	if (station_action=="1"):

		for i in station_to_modify:
			db.stations_states.delete_one({"_id":i["_id"]})

	elif(station_action=="2"):
		name=input("Nouvelle valeur pour name : (0 pour ne pas mettre à jour la donnée)")
		status=input("Nouvelle valeur pour status : (0 pour ne pas mettre à jour la donnée)")
		size=input("Nouvelle valeur pour size : (0 pour ne pas mettre à jour la donnée)")

		
		myqueryName={"$set" : {'name': name}}
		myqueryStatus={"$set" : {"status":status}}
		myquerySize={"$set" : {"size":int(size)}}
		
		for x in station_to_modify:
			if(name!="0"):
				db.stations_states.update_one({"_id": x["_id"]},myqueryName)
			if(status!="0"):
				db.stations_states.update_one({"_id": x["_id"]},myqueryStatus)
			if(size!="0"):
				db.stations_states.update_one({"_id": x["_id"]},myquerySize)

	else:
		return 1


def desactivateStation():
	lat=input("Entrez lat\n")
	lon=input("Entrez lon\n")
	dist=input("Entrez distance\n")
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


def get_stat(city):
	x=db.history.aggregate([
		{"$match":{"ville":city}},
		{"$match":{"size":{"$gt":0}}},
		{"$match":{"timestamp.day":{"$in":[0,1,2,3,4]}}},
		{"$match":{"timestamp.time":{"$eq":18}}},
		{"$project":{"_id":0,"ville":1,"name":1,"ratio":{"$divide":["$velo_available","$size"]},"velo_available":1,"place_available":1,"location":1,"status":1,"timestamp":1},
		},
		{"$match":{"ratio":{"$lt":0.20}}}
		])
	
	for i in x:
		print(i)

city=input("Quelle ville voulez-vous gérer ? (1) : LILLE | (2) : PARIS | (3) : LYON | (4) : RENNES ")
action=input("Que voulez-vous faire ? (1) : Chercher une station | (2) : Mettre à jour/supprimer une station | (3) : Désactiver une zone | (4) : Obtenir des statistique | (OTHER) : quitter")

if(city=="1"):
	city="Lille"
elif(city=="2"):
	city="Paris"
elif(city=="3"):
	city="Lyon"
elif(city=="4"):
	city="Rennes"


while(True):
	
	if( action =="1"):
		search_string=input("Quelle station cherchez-vous ? ")
		get_station_by_input(city,search_string)
		input_redo=input("Faire une nouvelle recherche ? (1) : OUI | (2) : NON | (OTHER) : QUIT ")

	elif(action=="2"):
		update_or_delete_station(city)
		input_redo=input("Faire une nouvelle mise à jour ou suppression ? (1) : OUI | (2) : NON | (OTHER) : QUIT ")

	elif(action=="3"):
		desactivateStation()
		input_redo=input("Faire modification sur une zone géographique ? (1) : OUI | (2) : NON | (OTHER) : QUIT ")

	elif(action=="4"):
		get_stat(city)
		input_redo=2

	else :
		break
	
	#next action
	if(input_redo=="2"):
		action=input("Que voulez-vous faire ? (1) : Chercher une station | (2) : Mettre à jour/supprimer une station | (3) : Désactiver une zone | (4) : Obtenir des statistique | (OTHER) : quitter")
	elif(input_redo!="1"):
		break
 
	
