# fapag_collecte_backend

Application web de collecte de fonds pour la République Gabonaise

## Fonctionnalités principales
- Gestion des cagnottes, participations, transactions, webhooks, actualités
- Authentification JWT, 2FA admin, permissions DRF
- Sécurité avancée (HSTS, CSP, CORS, CSRF, Axes, logging, audit)
- Tâches asynchrones (Celery + Redis)
- Stockage S3/MinIO pour reçus PDF et images
- PostgreSQL, sauvegardes chiffrées
- Monitoring/logging prêt pour SIEM

## Installation
1. Cloner le dépôt
2. Copier `.env.example` en `.env` et adapter les valeurs
3. Créer l'environnement virtuel et installer les dépendances :
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```
4. Lancer les migrations :
   ```bash
   python manage.py migrate
   ```
5. Créer un superutilisateur :
   ```bash
   python manage.py createsuperuser
   ```
6. Lancer le serveur :
   ```bash
   python manage.py runserver
   ```

## Structure
- `collecte/` : logique métier (modèles, vues, API)
- `fapag_collecte_backend/` : configuration principale

## Sécurité
- JWT courts, 2FA admin, throttling, HMAC webhooks, idempotence paiements
- Journalisation exhaustive, sauvegardes chiffrées, DB en réseau privé

## Tâches asynchrones
- Lancer le worker Celery :
  ```bash
  celery -A fapag_collecte_backend worker -l info
  ```

## Déploiement
- Prévu pour Gunicorn, Whitenoise, S3/MinIO, Redis, PostgreSQL
