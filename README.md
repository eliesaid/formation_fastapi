# 🚀 Formation FastAPI — Projet Fil Rouge & Exercices par Jour

## 🎯 Objectifs du projet
Ce dépôt sert de support à la formation et se compose de :
- Un **projet fil rouge** dans `app/` (API FastAPI complète)
- Des **exercices pratiques** par journée dans `test_jour1/`, `test_jour2/`, `test_jour3/`

Compétences travaillées :
- API REST avec **FastAPI**
- Validation des données (**Pydantic**)
- Persistance (**SQLAlchemy** + PostgreSQL)
- Sécurité (**OAuth2 + JWT**)
- Tests (**pytest**)
- Conteneurisation & déploiement (**Docker**, notions CI/CD)

---

## 🛠️ Installation & Lancement

### 1) Cloner le dépôt

```bash
git clone https://github.com/eliesaid/formation_fastapi.git
cd formation_fastapi

## 🛠️ Installation et configuration

### 1. Cloner le dépôt
```bash


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
│── .gitignore
│── venv/
│
├── test_jour1/              # Exercices J1 (bases FastAPI, routes, params)
│   ├── exercices/
│   └── solutions/
├── test_jour2/              # Exercices J2 (Pydantic, sécurité, SQLAlchemy)
│   ├── exercices/
│   └── solutions/
├── test_jour3/              # Exercices J3 (middlewares, tests, Docker)
│   ├── exercices/
│   └── solutions/
│
└── app/                     # Projet fil rouge (application principale)
    ├── __init__.py
    ├── main.py
    ├── routers/
    ├── models/
    ├── schemas/
    ├── core/
    └── tests/
    


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