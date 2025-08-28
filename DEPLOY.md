# Déploiement sur Render

Ce guide explique comment déployer l'application FAPAG Collecte sur Render.

## Prérequis

- Un compte [Render](https://render.com/)
- Un compte [Supabase](https://supabase.com/) (pour la base de données)
- Un dépôt Git (GitHub, GitLab ou Bitbucket)

## Configuration de la base de données

1. Créez une nouvelle base de données PostgreSQL sur Supabase
2. Récupérez l'URL de connexion dans les paramètres de la base de données
3. Assurez-vous que la base de données accepte les connexions depuis Render

## Configuration des variables d'environnement

Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```env
# Configuration de base
DEBUG=False
SECRET_KEY=votre_clé_secrète_très_longue_et_sécurisée
ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1

# Base de données (remplacez par vos informations)
DATABASE_URL=postgresql://user:password@host:port/dbname?sslmode=require

# Sécurité
CSRF_TRUSTED_ORIGINS=https://votre-app.onrender.com,http://localhost:3000
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True

# Fichiers statiques
STATIC_URL=/static/
STATIC_ROOT=staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=media
```

## Déploiement sur Render

1. **Créez un nouveau service Web** sur Render
   - Sélectionnez "Web Service"
   - Liez votre dépôt Git

2. **Configurez le service**
   - Nom : `fapag-collecte` (ou le nom de votre choix)
   - Région : `Frankfurt` (pour une meilleure latence en Europe)
   - Branche : `main` (ou votre branche de production)
   - Commande de build : `./build.sh`
   - Commande de démarrage : `gunicorn fapag_collecte_backend.wsgi:application`

3. **Variables d'environnement**
   - Ajoutez toutes les variables de votre fichier `.env`
   - Ajoutez `PYTHON_VERSION=3.9.10`
   - Ajoutez `PYTHONUNBUFFERED=True`

4. **Plan**
   - Sélectionnez le plan gratuit pour commencer
   - Mettez à jour vers un plan payant pour les environnements de production

## Après le déploiement

1. **Migrations de base de données**
   Les migrations s'exécutent automatiquement lors du déploiement grâce au script `build.sh`.

2. **Fichiers statiques**
   Les fichiers statiques sont collectés automatiquement lors du déploiement.

3. **Médias**
   Pour la production, il est recommandé d'utiliser un stockage externe comme AWS S3.

## Surveillance

- Les logs sont disponibles dans le tableau de bord Render
- Pour une surveillance avancée, configurez Sentry (optionnel)

## Mises à jour

Les mises à jour sont déployées automatiquement à chaque push sur la branche configurée.

## Dépannage

- **Erreurs de connexion à la base de données** : Vérifiez l'URL de connexion et les paramètres de sécurité
- **Fichiers statiques manquants** : Vérifiez que `collectstatic` s'est bien exécuté
- **Erreurs 500** : Consultez les logs dans le tableau de bord Render
