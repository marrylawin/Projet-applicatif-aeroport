# Système de gestion des vols et des passagers pour l'aéroport Charles de Gaulle
### Réalisé par : Marry Lawin, Verlie Aimé, Véronique Masuaku, Jean Michel Mupapa & Serena Marcelline
### Contexte

L’aéroport Charles de Gaulle modernise la gestion de ses informations relatives aux vols, aux passagers et aux services associés. Le système développé permet :

    - De gérer efficacement les données des vols, passagers et services
    - D’afficher ces informations sur des panneaux connectés
    - De proposer des recommandations de destinations basées sur l’historique des passagers grâce à la reconnaissance faciale

### Fonctionnalités principales

    - Opérations CRUD sur les vols, passagers et services
    - Recommandation intelligente de destinations basée sur les profils similaires
    - Reconnaissance faciale pour identifier un passager et déclencher des recommandations
    - Visualisation des données : taux de remplissage des vols, durée moyenne, parts de marché, etc
    - Génération de contenu d’e-mail personnalisé avec les suggestions de voyages (API simulée)

### Architecture de la base de données

**Base : ma_base_test**

**Collection : flights**
  
    - _id	= ID unique
    - flight_number =	Numéro de vol
    - departure	= Aéroport de départ
    - arrival	= Aéroport d’arrivée
    - duration = Durée (en minutes)
    - airline	= Compagnie aérienne
    - capacity	= Nombre de sièges
    - delayed =	Retard (en minutes)

**Collection : passengers**

    - _id	= ID unique
    - first_name	= Prénom
    - last_name	= Nom
    - email	= Email
    - flight_id =	Référence au vol (clé étrangère vers flights)

**Collection : services**

    - _id	= ID unique
    - flight_id	= Référence au vol
    - name	= Nom du service (ex : WiFi, Bagages, Embarquement)

**Collection : recommendations**

    - _id	= ID unique
    - passenger_id	= Référence au passager
    - flight_id	= Référence au vol recommandé

### Fonctionnalités techniques

**CRUD**

    - Ajouter / Modifier / Supprimer des vols, passagers et services

**Recommandation intelligente**

    - Basée sur les profils similaires
    - Pondération :
        - Destination (x2)
        - Compagnie (x1.5)
        - Durée (x1)
    - Exclusion des destinations déjà visitées

**Reconnaissance faciale**

    - Identification d’un passager via la caméra
    - Déclenche la génération de recommandations personnalisées


**Génération de contenu email :** 

    - Le système simule la préparation d’un email contenant les recommandations personnalisées d’un passager, activé après reconnaissance faciale

**Visualisation & Statistiques**

    - Taux de remplissage des vols
    - Durée moyenne des vols par compagnie
    - Parts de marché des compagnies
    - Répartition des passagers par vol
    - Nombre de vols par destination

### Installation

**Prérequis :**

    - Python
    - MongoDB (local ou cloud via MongoDB Atlas)
    - Librairies Python : pip install -r requirements.txt

**Fichier .env :**

    - MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority

**Lancer le projet**

    - python main.py

Sur MONGO.DB, après avoir fait vos commande de test comme "python main.py ou encore python crud.py, vous devriez voir afficher ceci :

<img width="1207" alt="Capture d’écran 2025-06-29 à 22 30 34" src="https://github.com/user-attachments/assets/d4991e85-0e89-448d-a6c9-78c3fcfe1b40" />
<img width="1226" alt="Capture d’écran 2025-06-29 à 22 28 36" src="https://github.com/user-attachments/assets/e2ddeba5-9d05-4fae-ba1d-77a83ac58e66" />
<img width="1219" alt="Capture d’écran 2025-06-29 à 22 29 48" src="https://github.com/user-attachments/assets/b207d580-266f-4be9-92c4-9c9e77d5e14e" />

### Structure du projet :

<img width="299" alt="Capture d’écran 2025-06-29 à 22 23 13" src="https://github.com/user-attachments/assets/13d17964-6697-478e-873b-534d326e31a7" />
