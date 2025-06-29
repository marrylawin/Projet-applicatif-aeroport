from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


#charger l'URI
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["ma_base_test"]



#FLIGHTS COLLECTION

flights = db["flights"]

def create_flight(flight):
    return flights.insert_one(flight)

def get_all_flights():
    return list(flights.find())

def get_flight_by_id(flight_id):
    from bson.objectid import ObjectId
    return flights.find_one({"_id": ObjectId(flight_id)})

def update_flight(flight_id, update_data):
    from bson.objectid import ObjectId
    return flights.update_one({"_id": ObjectId(flight_id)}, {"$set": update_data})

def delete_flight(flight_id):
    from bson.objectid import ObjectId
    return flights.delete_one({"_id": ObjectId(flight_id)})

#PASSAGERS COLLECTION

passengers = db["passengers"]

def create_passenger(passenger):
    return passengers.insert_one(passenger)

def get_all_passengers():
    return list(passengers.find())

def get_passenger_by_id(passenger_id):
    from bson.objectid import ObjectId
    return passengers.find_one({"_id": ObjectId(passenger_id)})

def update_passenger(passenger_id, update_data):
    from bson.objectid import ObjectId
    return passengers.update_one({"_id": ObjectId(passenger_id)}, {"$set": update_data})

def delete_passenger(passenger_id):
    from bson.objectid import ObjectId
    return passengers.delete_one({"_id": ObjectId(passenger_id)})

#SERVICES COLLECTION

services = db["services"]

def create_service(service):
    return services.insert_one(service)

def get_all_services():
    return list(services.find())

def get_services_by_flight(flight_id):
    from bson.objectid import ObjectId
    return list(services.find({"flight_id": ObjectId(flight_id)}))

def update_service(service_id, update_data):
    from bson.objectid import ObjectId
    return services.update_one({"_id": ObjectId(service_id)}, {"$set": update_data})

def delete_service(service_id):
    from bson.objectid import ObjectId
    return services.delete_one({"_id": ObjectId(service_id)})


#RECOMMANDATIONS PAR SIMILARITÉ

def get_recommendations_by_similarity_weighted(passenger_email, top_n=3):

    data = build_passenger_profiles()
    df = pd.DataFrame(data)

    if passenger_email not in df["_id"].values:
        return []

    df["dest"] = df["destinations"].apply(lambda x: " ".join(x))
    df["airline"] = df["airlines"].apply(lambda x: " ".join(x))
    df["duration"] = df["avg_duration"].apply(lambda d: str(int(d // 60)) if d else "0")

    #Pondération : destination x2, airline x1.5, duration x1
    df["profile"] = df["dest"] + " " + df["dest"] + " " + df["airline"] + " " + df["airline"] + " " + df["duration"]

    vec = CountVectorizer()
    X = vec.fit_transform(df["profile"])

    sim_matrix = cosine_similarity(X)
    idx_map = {email: idx for idx, email in enumerate(df["_id"])}
    target_idx = idx_map[passenger_email]

    similar_indices = sim_matrix[target_idx].argsort()[::-1][1:]

    visited = set(df.iloc[target_idx]["destinations"])
    recommendations = set()

    for idx in similar_indices:
        others = set(df.iloc[idx]["destinations"])
        new = others - visited
        recommendations.update(new)
        if len(recommendations) >= top_n:
            break

    return list(recommendations)[:top_n]

#ENREGISTRER LES RECOMMANDATIONS

def enregistrer_recommandations(passenger_email, recommandations):
    passenger = db["passengers"].find_one({"email": passenger_email})
    if not passenger:
        print("Passager introuvable.")
        return

    for dest in recommandations:
        vol = db["flights"].find_one({"arrival": dest})
        if vol:
            db["recommendations"].insert_one({
                "passenger_id": passenger["_id"],
                "flight_id": vol["_id"]
            })

#PASSENGER PROFILE

    #afficher les recommandations enregistrées
def get_passenger_profile(passenger_id):
    passenger = db["passengers"].find_one({"_id": ObjectId(passenger_id)})
    if not passenger:
        print("Passager introuvable.")
        return

    print(f"\n Profil du passager : {passenger['first_name']} {passenger['last_name']} ({passenger['email']})")

    #vols pris
    vols = db["flights"].find({"_id": {"$in": [p["flight_id"] for p in db["passengers"].find({"email": passenger["email"]})]}})
    print("\n Historique des vols :")
    for vol in vols:
        print(f"- {vol['departure']} vers {vol['arrival']} avec {vol['airline']}")

    #recommandations enregistrées
    print("\n Recommandations passées :")
    recommandations = db["recommendations"].find({"passenger_id": passenger["_id"]})
    found = False
    for r in recommandations:
        flight = db["flights"].find_one({"_id": r["flight_id"]})
        if flight:
            print(f"- {flight['arrival']} via {flight['airline']}")
            found = True
    if not found:
        print("Aucune recommandation enregistrée.")



#TROUVER DES PASSAGERS SIMILAIRES

def find_similar_passengers(passenger_id):
    from bson.objectid import ObjectId

    passenger = db["passengers"].find_one({"_id": ObjectId(passenger_id)})
    if not passenger:
        print("Passager introuvable.")
        return []

    flight = db["flights"].find_one({"_id": ObjectId(passenger["flight_id"])})
    if not flight:
        print("Vol introuvable.")
        return []

    #critères de comparaison
    target_airline = flight["airline"]
    target_arrival = flight["arrival"]
    target_duration = flight["duration"]

    #chercher d'autres passagers avec des critères similaires
    similar = db["passengers"].find({
        "_id": {"$ne": passenger["_id"]},
        "flight_id": {
            "$in": [
                f["_id"] for f in db["flights"].find({
                    "airline": target_airline,
                    "arrival": target_arrival,
                    "duration": {"$gte": target_duration - 30, "$lte": target_duration + 30}
                })
            ]
        }
    })

    return list(similar)

#GÉNÉRER AUTOMATIQUEMENT LE CONTENU D'UN EMAIL

def generate_email_content(passenger_id):
    passenger = db["passengers"].find_one({"_id": ObjectId(passenger_id)})
    if not passenger:
        return "Passager introuvable."

    first_name = passenger.get("first_name", "voyageur")

    #récupérer les recommandations
    recommendations = db["recommendations"].find({"passenger_id": ObjectId(passenger_id)})
    recommendations_list = list(recommendations)

    if recommendations_list:
        content = f"Bonjour {first_name},\n\n"
        content += "Nous avons déniché quelques destinations qui pourraient vous inspirer :\n\n"

        for r in recommendations_list:
            sugg = db["flights"].find_one({"_id": r["flight_id"]})
            if sugg:
                arrival = sugg.get("arrival", "une destination mystérieuse")
                airline = sugg.get("airline", "une compagnie partenaire")
                content += f"• {arrival} avec {airline}\n"

        content += "\n✨ Pour réserver ou en savoir plus, connectez-vous à votre espace client.\n"
        content += "À très bientôt dans les airs, avec nous ! 🛫"
    else:
        content = f"Bonjour {first_name},\n\n"
        content += "Pas encore de nouvelles recommandations pour vous aujourd’hui.\n"
        content += "Mais restez à l’écoute, des idées d’évasion arrivent bientôt ! 🌍"

    return content


#STATISTIQUES DE VOLS

def generate_flight_stats(flight_id):
    vol = db["flights"].find_one({"_id": ObjectId(flight_id)})
    if not vol:
        return f"Vol avec ID {flight_id} introuvable."

    #nombre total de passagers sur ce vol
    nb_passagers = db["passengers"].count_documents({"flight_id": ObjectId(flight_id)})

    #capacité du vol
    capacity = vol.get("capacity", None)
    if capacity:
        taux_remplissage = round((nb_passagers / capacity) * 100, 1)
    else:
        taux_remplissage = "inconnu"

    #retard (s’il y a)
    retard = vol.get("delayed", "non précisé")

    return {
        "vol": vol["flight_number"],
        "nb_passagers": nb_passagers,
        "capacity": capacity,
        "taux_remplissage (%)": taux_remplissage,
        "retard (min)": retard
    }

#ENRICHIR LES DONNÉES DES PASSAGERS
def build_passenger_profiles():
    pipeline = [
        {
            "$lookup": {
                "from": "flights",
                "localField": "flight_id",
                "foreignField": "_id",
                "as": "flight"
            }
        },
        {"$unwind": "$flight"},
        {
            "$group": {
                "_id": "$email",
                "destinations": {"$addToSet": "$flight.arrival"},
                "airlines": {"$addToSet": "$flight.airline"},
                "avg_duration": {"$avg": "$flight.duration"}
            }
        }
    ]
    return list(db["passengers"].aggregate(pipeline))


