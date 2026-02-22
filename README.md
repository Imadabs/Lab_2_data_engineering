Playstore Data Pipeline (Lab 2)
Ce projet implémente un pipeline de données complet pour collecter, transformer et exporter des données provenant du Google Play Store. Le projet utilise Python pour l'ingestion et l'exportation, SQLite comme base de données locale, et dbt pour la transformation des données.
+4

📂 Structure du Projet
Plaintext

lab 2/
├── ingest.py                 # Script d'ingestion des données brutes (JSONL -> DB)
├── export_to_powerbi.py      # Script d'exportation des données transformées
├── playstore_pipeline/       # Projet d'analyse de données (dbt)
│   ├── dbt_project.yml       # Configuration du projet dbt
│   ├── models/               # Modèles SQL (Marts, Dimensions, etc.)
│   │   └── marts/
│   │       └── dimensions/   # Modèles dim_categories, dim_date, etc.
│   ├── seeds/                # Données statiques chargées via dbt
│   ├── data/                 # Stockage des données
│   │   ├── raw/              # Fichiers bruts (apps.jsonl, reviews.jsonl)
│   │   └── db/               # Base de données SQLite (playstore.db)
│   └── tests/                # Tests de qualité des données
├── logs/                     # Journaux d'exécution de dbt
└── dbt_run_output.txt        # Résultat de la dernière exécution dbt
🚀 Fonctionnalités

Ingestion : Le script ingest.py charge les fichiers JSONL bruts (apps.jsonl, reviews.jsonl) dans une base de données SQLite locale nommée playstore.db.
+1

Transformation (dbt) : Utilisation de modèles SQL pour organiser les données en dimensions et faits :


dim_categories : Organisation des applications par catégorie.


dim_date : Table de temps pour les analyses chronologiques.


dim_developers : Informations sur les développeurs d'applications.
+2


Qualité des données : Des tests unique et not_null sont configurés pour garantir l'intégrité des clés primaires (ex: category_sk, date_key, developer_id).
+2

Export : Le script export_to_powerbi.py permet de préparer les données pour une visualisation externe.

🛠️ Installation et Utilisation
Prérequis
Python 3.x

dbt (adaptateur SQLite)

Étapes
Ingestion des données :

python ingest.py
Exécution du pipeline dbt :
Accédez au dossier du pipeline et exécutez les transformations :

cd playstore_pipeline
dbt run
Vérification de la qualité :

dbt test
Exportation :


python export_to_powerbi.py
📊 Visualisation
Une fois le pipeline exécuté, les modèles transformés dans playstore.db peuvent être connectés à Power BI ou tout autre outil de BI pour générer des rapports sur les performances des applications mobiles.
