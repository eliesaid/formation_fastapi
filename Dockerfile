# Étape 1 : image de base
FROM python:3.12-slim

# Étape 2 : définir le répertoire de travail
WORKDIR /app

# Étape 3 : installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose le port utilisé par Uvicorn
EXPOSE 8000

# Étape 4 : copier tout le code
COPY . .

# Étape 5 : commande de lancement (depuis la racine, avec app.main)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

