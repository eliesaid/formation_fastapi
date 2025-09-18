# 🚀 Formation FastAPI — Projet Fil Rouge & Exemples par Jour

## 🎯 Objectifs du projet
Ce dépôt sert de support à la formation et se compose de :
- Un **projet fil rouge** dans `app/` (API FastAPI complète, évolutive sur 3 jours)
- Des **exemples pratiques** par journée dans `test_jour1/`, `test_jour2/`, `test_jour3/`

Compétences travaillées :
- API REST avec **FastAPI**
- Validation des données (**Pydantic**)
- Persistance (**SQLAlchemy** + PostgreSQL)
- Sécurité (**OAuth2 + JWT**)
- Tests (**pytest**)
- Conteneurisation & déploiement (**Docker**, notions CI/CD)

---

## 🛠️ Installation & Lancement

### 1. Cloner le dépôt
```bash
git clone https://github.com/eliesaid/formation_fastapi.git
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

🐳 Docker

Construire une image avec Docker

docker build -t image-api .
docker run -d -p 8000:8000 --name api-container image-api

Arrêter le conteneur :

docker stop api-container

Avec docker-compose

docker-compose up --build -d
docker-compose down

📂 Arborescence du projet

formation_fastapi/
│── README.md
│── requirements.txt
│── .gitignore
│── venv/
│
├── test_jour1/              # Exemples Jour 1 (bases FastAPI, routes, params)
├── test_jour2/              # Exemples Jour 2 (Pydantic, sécurité, SQLAlchemy)
├── test_jour3/              # Exemples Jour 3 (middlewares, tests, Docker)
│
└── app/                     # Projet fil rouge (application principale)
    ├── __init__.py
    ├── main.py
    ├── routers/
    ├── models/
    ├── schemas/
    ├── core/
    └── tests/

### 🚧 Étapes du projet (progression de la formation) ###

Mise en place du projet  avec FastAPI

Création de routes (GET, POST, Path Params, Query Params)

Validation avec Pydantic

Sécurité et Authentification (JWT, OAuth2, Hashage mots de passe)

Connexion à une base PostgreSQL avec SQLAlchemy

Mise en place des Midlleware et des Tasks

Tests avec pytest

Conteneurisation avec Docker

Déploiement (Gunicorn, Docker Compose, CI/CD GitHub Actions)