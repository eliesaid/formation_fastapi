# 🚀 Formation FastAPI — Projet Fil Rouge

## 🎯 Objectifs du projet
Ce projet est utilisé comme fil rouge tout au long de la formation.  
Les apprenants vont apprendre à :
- Créer une API REST avec **FastAPI**  
- Structurer un projet Python de manière professionnelle  
- Utiliser **Uvicorn** comme serveur de développement  
- Mettre en place la validation des données avec **Pydantic**  
- Connecter une base de données (PostgreSQL + SQLAlchemy)  
- Sécuriser l’API avec OAuth2 et JWT  
- Écrire des tests avec **pytest**  
- Conteneuriser et déployer avec **Docker**  

---

## 🛠️ Installation et configuration

### 1. Cloner le dépôt
```bash

git clone https://github.com/votre-org/formation_fastapi.git
cd formation_fastapi
2. Créer et activer un environnement virtuel (Ubuntu)


sudo apt update
sudo apt install python3.12-venv -y

python3 -m venv venv
source venv/bin/activate
3. Installer les dépendances

pip install --upgrade pip
pip install -r requirements.txt
4. Lancer le serveur


uvicorn app.main:app --reload
API disponible sur : http://127.0.0.1:8000

Documentation interactive Swagger : http://127.0.0.1:8000/docs

Documentation alternative ReDoc : http://127.0.0.1:8000/redoc

📂 Arborescence du projet

formation_fastapi/
│── README.md                
│── requirements.txt         
│── venv/                    
│
└── app/                     
    │── __init__.py
    │── main.py              
    │── routers/             
    │── models/              
    │── schemas/             
    │── core/                
    │── tests/               


    ### 🚧 Étapes du projet (progression de la formation)

# 1. Mise en place du projet & Hello World avec FastAPI

# 2. Création de routes (GET, POST, Path Params, Query Params)

# 3. Validation avec Pydantic

# 4. Sécurité et Authentification (JWT, OAuth2, Hashage mots de passe)

# 5. Connexion à une base PostgreSQL avec SQLAlchemy

# 6. Tests avec pytest

# 7. Conteneurisation avec Docker

# 8. Déploiement (Gunicorn, Docker Compose, CI/CD GitHub Actions)

""" 🤝 Contribution

Chaque apprenant aura sa branche GitHub pour travailler sur ses propres exercices.
Des corrections seront proposées par le formateur sur des branches dédiées"""