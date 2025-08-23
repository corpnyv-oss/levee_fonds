# Documentation Technique - Application de Collecte de Fonds

## Architecture Technique

### Stack Technologique
- **Backend**: Django 5.2.5
- **Base de données**: PostgreSQL
- **Cache**: Redis
- **File d'attente**: Celery
- **Authentification**: JWT + 2FA
- **Frontend**: (À définir)

### Structure du Projet

```
backend/
├── collecte/                  # Application principale
│   ├── migrations/           # Migrations de la base de données
│   ├── payments/             # Intégrations de paiement
│   ├── templates/            # Templates HTML
│   ├── tests/                # Tests unitaires
│   ├── utils/                # Utilitaires
│   ├── __init__.py
│   ├── admin.py              # Interface d'administration
│   ├── apps.py
│   ├── models.py             # Modèles de données
│   ├── serializers.py        # Sérialiseurs DRF
│   ├── urls.py               # Routes de l'API
│   └── views.py              # Vues de l'API
├── fapag_collecte_backend/   # Configuration du projet
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py          # Configuration
│   ├── urls.py             # URLs principales
│   └── wsgi.py
├── docs/                    # Documentation
└── tests/                   # Tests d'intégration
```

## Installation

### Prérequis
- Python 3.9+
- PostgreSQL
- Redis
- ClamAV (optionnel pour l'analyse antivirus)

### Configuration

1. Cloner le dépôt
2. Créer un environnement virtuel
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```
3. Installer les dépendances
   ```bash
   pip install -r requirements.txt
   ```
4. Configurer les variables d'environnement
   ```bash
   cp .env.example .env
   # Éditer .env avec vos paramètres
   ```
5. Appliquer les migrations
   ```bash
   python manage.py migrate
   ```
6. Créer un superutilisateur
   ```bash
   python manage.py createsuperuser
   ```
7. Lancer le serveur de développement
   ```bash
   python manage.py runserver
   ```

## API Documentation

L'API est documentée avec Swagger/OpenAPI. Accédez à la documentation à l'adresse :
`http://localhost:8000/api/docs/`

## Tests

### Lancer les tests unitaires
```bash
pytest
```

### Lancer les tests d'intégration
```bash
pytest tests/
```

### Couverture de code
```bash
pytest --cov=collecte tests/
```

## Déploiement

### Production
Pour le déploiement en production, utilisez un serveur WSGI comme Gunicorn avec un reverse proxy comme Nginx.

### Variables d'environnement critiques
- `SECRET_KEY`: Clé secrète Django
- `DATABASE_URL`: URL de connexion à la base de données
- `REDIS_URL`: URL de connexion à Redis
- `EMAIL_*`: Configuration SMTP
- `ALLOWED_HOSTS`: Liste des hôtes autorisés

## Sécurité

### Mesures de sécurité implémentées
- Authentification forte (2FA)
- Protection CSRF
- En-têtes de sécurité HTTP
- Validation des entrées
- Journalisation des actions sensibles
- Chiffrement des données sensibles

### Audit de sécurité
Pour effectuer un audit de sécurité :
```bash
bandit -r .
safety check
```

## Maintenance

### Sauvegardes
Les sauvegardes sont configurées pour s'exécuter quotidiennement. Utilisez :
```bash
python manage.py dbbackup
```

### Mises à jour
1. Mettre à jour les dépendances :
   ```bash
   pip install -r requirements.txt --upgrade
   ```
2. Appliquer les migrations :
   ```bash
   python manage.py migrate
   ```
3. Redémarrer les services

## Support
Pour toute question ou problème, contactez l'équipe de développement.
