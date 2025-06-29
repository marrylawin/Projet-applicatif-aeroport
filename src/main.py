from pymongo import MongoClient
from dotenv import load_dotenv
import os
import random
from bson.objectid import ObjectId
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd


#charger les variables d'environnement
load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["ma_base_test"]

#nettoyage des collections #on a fait ça car à force d'executer le code ça faisait des doublons
db["flights"].delete_many({})
db["passengers"].delete_many({})
db["utilisateurs"].delete_many({})
db["services"].delete_many({})
db["passengers"].delete_one({"_id": ObjectId("685abc3d22a293fbb6950cdf")})

print("Toutes les collections ont été vidées proprement.")

#recharger les variables d'environnement depuis le fichier .env
load_dotenv()

#récupérer l'URI MongoDB
mongo_uri = os.getenv("MONGO_URI")

#se connecter à MongoDB
client = MongoClient(mongo_uri)

#TEST

#accéder à ta base
db = client["ma_base_test"]
print("Connexion réussie à MongoDB")

#accéder à une collection (comme une table dans une base SQL)
collection = db["utilisateurs"]

#créer un document à insérer
utilisateur = {
    "nom": "Marry",
    "email": "marrylawin@live.fr",
    "inscrit": True
}

#insérer le document
resultat = collection.insert_one(utilisateur)
print(f" Document inséré avec l'ID : {resultat.inserted_id}")

#DÉBUT

#FLIGHTS COLLECTION

#CRÉER

from crud import create_flight, get_all_flights

#liste des vols à insérer

vols = [
    {   
        "_id": ObjectId("685abeea25a646ae69be4e76"),
        "flight_number": "AF123",
        "departure": "Paris",
        "arrival": "New York",
        "duration": 480,
        "airline": "Air France",
        "capacity": 180,
        "delayed": 10
    },
    {
        "_id": ObjectId("685abeeb25a646ae69be4e77"),
        "flight_number": "BA456",
        "departure": "Londres",
        "arrival": "Tokyo",
        "duration": 720,
        "airline": "British Airways",
        "capacity": 100,
        "delayed": 30
    },
    {
        "_id": ObjectId("685abeeb25a646ae69be4e78"),
        "flight_number": "LH789",
        "departure": "Berlin",
        "arrival": "Rome",
        "duration": 120,
        "airline": "Lufthansa",
        "capacity": 230,
        "delayed": 80
    },
    {
        "_id": ObjectId("685abeeb25a646ae69be4e79"),
        "flight_number": "DL101",
        "departure": "Atlanta",
        "arrival": "Los Angeles",
        "duration": 300,
        "airline": "Delta Airlines",
        "capacity": 280,
        "delayed": 25
    },
    {
        "_id": ObjectId("685abeeb25a646ae69be4e7a"),
        "flight_number": "UA202",
        "departure": "Chicago",
        "arrival": "San Francisco",
        "duration": 240,
        "airline": "United Airlines",
        "capacity": 150,
        "delayed": 0
    },
    {
        "_id": ObjectId("685abeeb25a646ae69be4e7b"),
        "flight_number": "EK303",
        "departure": "Dubai",
        "arrival": "Sydney",
        "duration": 900,
        "airline": "Emirates",
        "capacity": 300,
        "delayed": 60
    },
    {
        "_id": ObjectId("685abeeb25a646ae69be4e7c"),
        "flight_number": "QR404",
        "departure": "Doha",
        "arrival": "Bangkok",
        "duration": 420,
        "airline": "Qatar Airways",
        "capacity": 100,
        "delayed": 15
    },
    {
        "_id": ObjectId("685abeeb25a646ae69be4e7d"),
        "flight_number": "SQ505",
        "departure": "Singapour",
        "arrival": "Johannesburg",
        "duration": 660,
        "airline": "Singapore Airlines",
        "capacity": 290,
        "delayed": 50
    },
    {
        "_id": ObjectId("685abeeb25a646ae69be4e7e"),
        "flight_number": "AC606",
        "departure": "Toronto",
        "arrival": "Vancouver",
        "duration": 300,
        "airline": "Air Canada",
        "capacity": 180,
        "delayed": 10
    },
    {
        "_id": ObjectId("685abeeb25a646ae69be4e7f"),
        "flight_number": "IB707",
        "departure": "Madrid",
        "arrival": "Lisbonne",
        "duration": 90,
        "airline": "Iberia",
        "capacity": 100,
        "delayed": 30
    },
    {
        "_id": ObjectId("6861781e27268cf7e19165fb"),
        "flight_number": "AF124",
        "departure": "Paris",
        "arrival": "New York",
        "duration": 500,
        "airline": "Air France",
        "capacity": 130,
        "delayed": 20
    },
    {
        "_id": ObjectId("6861781e27268cf7e19165fc"),
        "flight_number": "DL102",
        "departure": "Atlanta",
        "arrival": "Los Angeles",
        "duration": 310,
        "airline": "Delta Airlines",
        "capacity": 200,
        "delayed": 5
    },
    {
        "_id": ObjectId("6861781e27268cf7e19165fd"),
        "flight_number": "UA203",
        "departure": "Chicago",
        "arrival": "San Francisco",
        "duration": 245,
        "airline": "United Airlines",
        "capacity": 160,
        "delayed": 0
    },
    {
        "_id": ObjectId("6861781e27268cf7e19165fe"),
        "flight_number": "EK304",
        "departure": "Dubai",
        "arrival": "Sydney",
        "duration": 890,
        "airline": "Emirates",
        "capacity": 320,
        "delayed": 45
    },
    {
        "_id": ObjectId("6861781e27268cf7e19165ff"),
        "flight_number": "BA457",
        "departure": "Londres",
        "arrival": "Tokyo",
        "duration": 710,
        "airline": "British Airways",
        "capacity": 110,
        "delayed": 35
    }
]

#insérer chaque vol un par un
for v in vols:
    db["flights"].insert_one(v)

#afficher tous les vols
flights = get_all_flights()
print("Tous les vols :")
for f in flights:
    print(f)

#RÉCUPÉRER UN VOL PAR ID

id_test = "685a8d7c7d1735e680565ee4"

from crud import get_flight_by_id

id_test = "685a8d7c7d1735e680565ee1"  
flight = get_flight_by_id(id_test)
print("Vol récupéré par ID :")
print(flight)


#METTRE À JOUR UN VOL

from crud import update_flight

update_result = update_flight(id_test, {"duration": 999})
print(f"Vol mis à jour ? {update_result.modified_count} document(s) modifié(s)")


#SUPPRIMER UN VOL

from crud import delete_flight

delete_result = delete_flight(id_test)
print(f"Vol supprimé ? {delete_result.deleted_count} document(s) supprimé(s)")


#PASSAGERS COLLECTION

from crud import create_passenger, get_all_passengers

flight_id = ObjectId("685abeea25a646ae69be4e76") 

new_passengers = [
    {"first_name": "Alice", "last_name": "Durand", "email": "alice.durand@email.com", "flight_id": flight_id},
    {"first_name": "Jean", "last_name": "Dupont", "email": "jean.dupont@email.com", "flight_id": flight_id},
    {"first_name": "Marie", "last_name": "Curie", "email": "marie.curie@email.com", "flight_id": flight_id},
    {"first_name": "Lucas", "last_name": "Martin", "email": "lucas.martin@email.com", "flight_id": flight_id},
    {"first_name": "Emma", "last_name": "Lemoine", "email": "emma.lemoine@email.com", "flight_id": flight_id},
    {"first_name": "Nora", "last_name": "Benali", "email": "nora.benali@email.com", "flight_id": flight_id},
    {"first_name": "Olivier", "last_name": "Girard", "email": "olivier.girard@email.com", "flight_id": flight_id},
    {"first_name": "Camille", "last_name": "Petit", "email": "camille.petit@email.com", "flight_id": flight_id},
    {"first_name": "Sofia", "last_name": "Rossi", "email": "sofia.rossi@email.com", "flight_id": flight_id},
    {"first_name": "Thomas", "last_name": "Nguyen", "email": "thomas.nguyen@email.com", "flight_id": flight_id}
]

for passenger in new_passengers:
    res = create_passenger(passenger)
    print(f"Passager {passenger['first_name']} {passenger['last_name']} ajouté avec ID : {res.inserted_id}")


flight_id2 = ObjectId("685abeeb25a646ae69be4e77")

new_passengers = [
    {"first_name": "Noé", "last_name": "Lelavois", "email": "noe.lelavois@email.com", "flight_id": flight_id2},
    {"first_name": "Mark", "last_name": "Lawin", "email": "mark.lawin@email.com", "flight_id": flight_id2},
    {"first_name": "Maider", "last_name": "Saubade", "email": "maider.saubade@email.com", "flight_id": flight_id2},
    {"first_name": "Claire", "last_name": "Saubade", "email": "claire.saubade@email.com", "flight_id": flight_id2},
    {"first_name": "Leyna", "last_name": "Dore", "email": "leyna.dore@email.com", "flight_id": flight_id2},
    {"first_name": "Kelyan", "last_name": "Brunel", "email": "kelyan.brunel@email.com", "flight_id": flight_id2},
    {"first_name": "Carl", "last_name": "Jean", "email": "carl.jean@email.com", "flight_id": flight_id2},
    {"first_name": "Kenny", "last_name": "Coin", "email": "kenny.coin@email.com", "flight_id": flight_id2},
    {"first_name": "Alexis", "last_name": "Lakoue", "email": "alexis.lakoue@email.com", "flight_id": flight_id2},
    {"first_name": "Romain", "last_name": "Huys", "email": "romain.huys@email.com", "flight_id": flight_id2}
]

new__flight_id = ObjectId("685abeeb25a646ae69be4e7a")

new_passengers = [
    {"first_name": "Noé", "last_name": "Lelavois", "email": "noe.lelavois@email.com", "flight_id": new__flight_id},
    {"first_name": "Mark", "last_name": "Lawin", "email": "mark.lawin@email.com", "flight_id": new__flight_id},
    {"first_name": "Maider", "last_name": "Saubade", "email": "maider.saubade@email.com", "flight_id": new__flight_id},
    {"first_name": "Claire", "last_name": "Saubade", "email": "claire.saubade@email.com", "flight_id": new__flight_id},
    {"first_name": "Leyna", "last_name": "Dore", "email": "leyna.dore@email.com", "flight_id": new__flight_id},
    {"first_name": "Nora", "last_name": "Benali", "email": "nora.benali@email.com", "flight_id": new__flight_id},
    {"first_name": "Olivier", "last_name": "Girard", "email": "olivier.girard@email.com", "flight_id": new__flight_id},
    {"first_name": "Camille", "last_name": "Petit", "email": "camille.petit@email.com", "flight_id": new__flight_id},
    {"first_name": "Sofia", "last_name": "Rossi", "email": "sofia.rossi@email.com", "flight_id": new__flight_id},
    
]

#AJOUTER DE NOUVEAUX PASSAGERS

from crud import create_passenger

first_names = ["Alex", "Charlie", "Jordan", "Taylor", "Morgan", "Riley", "Casey", "Skyler", "Jamie", "Cameron"]
last_names = ["Smith", "Johnson", "Brown", "Williams", "Jones", "Garcia", "Martinez", "Davis", "Lopez", "Anderson"]

flight_ids = [
    ObjectId("685abeea25a646ae69be4e76"),
    ObjectId("685abeeb25a646ae69be4e77"),
    ObjectId("685abeeb25a646ae69be4e78"),
    ObjectId("685abeeb25a646ae69be4e79"),
    ObjectId("685abeeb25a646ae69be4e7a"),
    ObjectId("685abeeb25a646ae69be4e7b"),
    ObjectId("685abeeb25a646ae69be4e7c"),
    ObjectId("685abeeb25a646ae69be4e7d"),
    ObjectId("685abeeb25a646ae69be4e7e"),
    ObjectId("685abeeb25a646ae69be4e7f"),
    ObjectId("6861781e27268cf7e19165fb"),
    ObjectId("6861781e27268cf7e19165fc"),
    ObjectId("6861781e27268cf7e19165fd"),
    ObjectId("6861781e27268cf7e19165fe"),
    ObjectId("6861781e27268cf7e19165ff")
]

#récupérer tous les vols depuis la bdd
vols = list(db["flights"].find({}))

#pour chaque vol j'insère un nombre de passagers réaliste
for vol in vols:
    flight_id = vol["_id"]
    capacity = vol.get("capacity", 0)  #on récupère la capacité depuis le vol

    if capacity > 0:
        nb_passagers = random.randint(int(capacity * 0.5), capacity)  #remplissage entre 50% et 100%
        for i in range(nb_passagers):
            first = random.choice(first_names)
            last = random.choice(last_names)
            email = f"{first.lower()}.{last.lower()}{i}@email.com"
            passenger = {
                "first_name": first,
                "last_name": last,
                "email": email,
                "flight_id": flight_id
            }
            res = create_passenger(passenger)
            print(f"[{vol['flight_number']}] Passager {first} {last} inséré avec ID : {res.inserted_id}")
    else:
        print(f"⚠️ Capacité manquante pour le vol {vol.get('flight_number', 'Inconnu')} -> Aucun passager généré")

#SERVICES COLLECTION

from crud import create_service

default_services = [
    "WiFi à bord",
    "Repas végétarien",
    "Siège XL",
    "Films en HD",
    "Accès au salon VIP"
]

#récupérer tous les vols
all_flights = db["flights"].find()

#pour chaque vol ajouter les services
for flight in all_flights:
    for service_name in default_services:
        service = {"name": service_name, "flight_id": flight["_id"]}
        create_service(service)
        print(f"Ajouté : {service_name} au vol {flight['flight_number']}")



#mise à jour des vols avec enrichissements pour gérer les retards etc
enrichissements = {
    "685abeea25a646ae69be4e76": {"capacity": 180, "delayed": 10},
    "685abeeb25a646ae69be4e77": {"capacity": 220, "delayed": 0},
    "685abeeb25a646ae69be4e78": {"capacity": 150, "delayed": 20},
    "685abeeb25a646ae69be4e79": {"capacity": 200, "delayed": 5},
    "685abeeb25a646ae69be4e7a": {"capacity": 170, "delayed": 15},
    "685abeeb25a646ae69be4e7b": {"capacity": 300, "delayed": 25},
    "685abeeb25a646ae69be4e7c": {"capacity": 280, "delayed": 0},
    "685abeeb25a646ae69be4e7d": {"capacity": 250, "delayed": 30},
    "685abeeb25a646ae69be4e7e": {"capacity": 190, "delayed": 8},
    "685abeeb25a646ae69be4e7f": {"capacity": 160, "delayed": 0},
    "6861781e27268cf7e19165fb": {"capacity": 180, "delayed": 12},
    "6861781e27268cf7e19165fc": {"capacity": 220, "delayed": 0},
    "6861781e27268cf7e19165fd": {"capacity": 150, "delayed": 18},
    "6861781e27268cf7e19165fe": {"capacity": 200, "delayed": 7},
    "6861781e27268cf7e19165ff": {"capacity": 170, "delayed": 22}
}

#mise à jour des vols
for flight_id, update_data in enrichissements.items():
    result = db["flights"].update_one(
        {"_id": ObjectId(flight_id)},
        {"$set": update_data}
    )
    print(f"Vol {flight_id} mis à jour ({result.modified_count} champ(s) modifié(s))")


#statistiques sur les vols
from crud import get_recommendations_by_similarity_weighted, enregistrer_recommandations, get_passenger_profile, generate_email_content, generate_flight_stats
from facial_recognition.facial_recognition import identify_passenger_by_face

 #statistiques de tous les vols
vols = db["flights"].find()
print("\nStatistiques de tous les vols :")
for vol in vols:
    stats = generate_flight_stats(vol["_id"])
    for k, v in stats.items():
        print(f"{k} : {v}")
    print("-" * 40)

#identification d'un passager via reconnaissance faciale
email_detected = identify_passenger_by_face()


if email_detected:
    print(f"\nPassager détecté : {email_detected}")

    #générer des recommandations personnalisées
    suggestions = get_recommendations_by_similarity_weighted(email_detected)
    print("\n Recommandations :")
    for s in suggestions:
        print(f"- {s}")

    enregistrer_recommandations(email_detected, suggestions)

from crud import find_similar_passengers

#profil passager
passenger = db["passengers"].find_one({"email": email_detected})
if passenger:
    get_passenger_profile(passenger["_id"])

    #passagers similaires
    results = find_similar_passengers(passenger["_id"])
    print("\nProfils similaires :")
    for r in results:
        print(f"- {r['first_name']} {r['last_name']} ({r['email']})")


    #sénérer le contenu de l'email
    email_content = generate_email_content(passenger["_id"])
    print("\nContenu de l'email :\n")
    print(email_content)

else:
    print("Aucun visage reconnu. Aucune action effectuée.")

#STATISTIQUES GRAPHIQUES

#REMPLISSAGE DES VOLS

def plot_taux_remplissage():
    vols = list(db["flights"].find({}))
    noms_vols = []
    taux_remplissage = []

    for vol in vols:
        flight_id = vol["_id"]
        capacity = vol.get("capacity", 0)
        nb_passagers = db["passengers"].count_documents({"flight_id": flight_id})

        if capacity > 0:
            taux = round((nb_passagers / capacity) * 100, 1)
        else:
            taux = 0

        noms_vols.append(vol["flight_number"])
        taux_remplissage.append(taux)

    plt.figure(figsize=(10, 6))
    plt.bar(noms_vols, taux_remplissage, color='skyblue')
    plt.ylabel("Taux de remplissage (%)")
    plt.title("Taux de remplissage par vol")
    plt.ylim(0, 100)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

plot_taux_remplissage()


#DURÉE MOYENNE DES VOLS PAR COMPAGNIE : Pour comparer les offres

flights = list(db["flights"].find())
df = pd.DataFrame(flights)

moyennes = df.groupby("airline")["duration"].mean().sort_values()
moyennes.plot(kind="barh", color="skyblue", title="Durée moyenne des vols par compagnie")
plt.xlabel("Durée (minutes)")
plt.tight_layout()
plt.show()


#HISTOGRAMME DES PASSAGERS PAR VOL : Pour observer la distribution

vol_ids = [str(f["_id"]) for f in db["flights"].find()]
count_data = db["passengers"].aggregate([
    {"$group": {"_id": "$flight_id", "nb_passagers": {"$sum": 1}}}
])
counts = {str(c["_id"]): c["nb_passagers"] for c in count_data}

labels = []
values = []

for flight in db["flights"].find():
    fid = str(flight["_id"])
    labels.append(flight["flight_number"])
    values.append(counts.get(fid, 0))

plt.figure(figsize=(10, 5))
plt.bar(labels, values, color="lightgreen")
plt.ylabel("Nombre de passagers")
plt.title("Répartition des passagers par vol")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#PARTS DE MARCHÉ DES COMPAGNIES AÉRIENNES : vue d'ensemble des parts de marché
airline_counts = {}

cursor = db["passengers"].aggregate([
    {
        "$lookup": {
            "from": "flights",
            "localField": "flight_id",
            "foreignField": "_id",
            "as": "flight"
        }
    },
    {"$unwind": "$flight"},
    {"$group": {
        "_id": "$flight.airline",
        "count": {"$sum": 1}
    }}
])

for doc in cursor:
    airline_counts[doc["_id"]] = doc["count"]

labels = list(airline_counts.keys())
sizes = list(airline_counts.values())

plt.figure(figsize=(6, 6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title("Parts de marché des compagnies (selon les passagers)")
plt.tight_layout()
plt.show()


#NOMBRE DE VOLS PAR DESTINATION : pour visualiser les destinations les plus populaires

#récupérer les données : nombre de vols par destination
pipeline = [
    {"$group": {"_id": "$arrival", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
]
results = list(db["flights"].aggregate(pipeline))

#extraire les données pour le graphique
destinations = [res["_id"] for res in results]
nb_vols = [res["count"] for res in results]

plt.figure(figsize=(10, 6))
plt.bar(destinations, nb_vols, color='coral')
plt.title("Nombre de vols par destination")
plt.xlabel("Destination")
plt.ylabel("Nombre de vols")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()