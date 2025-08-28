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

Consultez le [guide de déploiement](DEPLOYMENT.md) pour des instructions détaillées sur le déploiement sur Render ou Railway.

### Variables d'environnement requises

Créez un fichier `.env` à la racine du projet avec les variables suivantes (voir `.env.example` pour un exemple complet) :

```bash
# Configuration de base
DEBUG=False
SECRET_KEY=votre_secret_key_tres_long_et_securise
ALLOWED_HOSTS=.yourdomain.com,localhost,127.0.0.1

# Base de données
DATABASE_URL=postgresql://user:password@host:port/dbname

# Configuration CORS
CORS_ALLOWED_ORIGINS=https://votre-frontend.com,http://localhost:3000

# Configuration du stockage (optionnel)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_STORAGE_BUCKET_NAME=your_bucket_name
```

### Commandes de déploiement rapide

1. **Migration de la base de données** :
   ```bash
   python manage.py migrate
   ```

2. **Collecte des fichiers statiques** :
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Lancement du serveur de production** :
   ```bash
   gunicorn fapag_collecte_backend.wsgi:application
   ```

Pour une configuration complète, reportez-vous au [guide de déploiement](DEPLOYMENT.md).
