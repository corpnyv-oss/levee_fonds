# Guide de déploiement FAPAG Collecte

Ce guide explique comment déployer l'application FAPAG Collecte sur Render et Railway.

## Prérequis

- Un compte [GitHub](https://github.com/)
- Un compte [Render](https://render.com/) ou [Railway](https://railway.app/)
- Une base de données PostgreSQL (fournie par Render, Railway ou Supabase)
- Un compte [Supabase](https://supabase.com/) (optionnel, pour la base de données)

## 1. Préparation du dépôt

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/fapag-collecte.git
   cd fapag-collecte
   ```

2. Créez un environnement virtuel et activez-le :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Créez un fichier `.env` basé sur `.env.example` et configurez-le :
   ```bash
   cp .env.example .env
   # Éditez le fichier .env avec vos paramètres
   ```

## 2. Déploiement sur Render

### Configuration du service Web

1. Connectez-vous à [Render](https://dashboard.render.com/)
2. Cliquez sur "New +" puis sélectionnez "Web Service"
3. Liez votre dépôt GitHub
4. Configurez le service :
   - **Name** : fapag-collecte (ou le nom de votre choix)
   - **Region** : Sélectionnez la région la plus proche de vos utilisateurs
   - **Branch** : main (ou votre branche de production)
   - **Build Command** : `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command** : `gunicorn fapag_collecte_backend.wsgi:application`

### Variables d'environnement

Ajoutez les variables d'environnement nécessaires dans la section "Environment Variables" :

```
DJANGO_SETTINGS_MODULE=fapag_collecte_backend.production_settings
SECRET_KEY=votre_secret_key_tres_long_et_securise
DEBUG=False
ALLOWED_HOSTS=*  # À remplacer par votre domaine en production
DATABASE_URL=postgresql://user:password@host:port/dbname
# Ajoutez les autres variables nécessaires depuis .env
```

### Configuration de la base de données

1. Dans le tableau de bord Render, allez dans "New +" > "PostgreSQL"
2. Configurez votre base de données et notez les informations de connexion
3. Mettez à jour la variable `DATABASE_URL` dans les variables d'environnement

### Déploiement

1. Cliquez sur "Create Web Service"
2. Render va maintenant construire et déployer votre application

## 3. Déploiement sur Railway

### Configuration du projet

1. Installez l'interface en ligne de commande Railway :
   ```bash
   npm i -g @railway/cli
   ```

2. Connectez-vous :
   ```bash
   railway login
   ```

3. Créez un nouveau projet :
   ```bash
   railway init fapag-collecte
   ```

4. Liez votre dépôt GitHub ou poussez votre code :
   ```bash
   git add .
   git commit -m "Préparation pour le déploiement"
   git push railway main
   ```

### Configuration des variables d'environnement

1. Allez dans l'onglet "Variables" de votre projet Railway
2. Ajoutez les variables nécessaires (les mêmes que dans .env.example)
3. Assurez-vous que `DJANGO_SETTINGS_MODULE` est défini sur `fapag_collecte_backend.production_settings`

### Configuration de la base de données

1. Dans Railway, allez dans l'onglet "Data"
2. Cliquez sur "New" et sélectionnez "PostgreSQL"
3. Une fois créée, la variable `DATABASE_URL` sera automatiquement ajoutée à vos variables d'environnement

### Déploiement

1. Votre application sera automatiquement déployée lorsque vous poussez des modifications sur la branche liée
2. Vous pouvez également déclencher un déploiement manuel depuis le tableau de bord

## 4. Configuration du domaine personnalisé (optionnel)

### Sur Render
1. Allez dans les paramètres de votre service web
2. Dans "Custom Domains", ajoutez votre domaine
3. Suivez les instructions pour configurer les enregistrements DNS

### Sur Railway
1. Allez dans l'onglet "Settings" de votre projet
2. Dans "Domains", ajoutez votre domaine personnalisé
3. Suivez les instructions pour configurer les enregistrements DNS

## 5. Mise à jour de l'application

Pour mettre à jour l'application après des modifications :

1. Poussez vos modifications sur la branche principale
2. Render/Railway détectera automatiquement les changements et redéploiera l'application
3. Pour les mises à jour de la base de données, exécutez :
   ```bash
   python manage.py migrate
   ```

## Dépannage

### Les migrations ne s'appliquent pas
Assurez-vous que la commande de migration est exécutée au démarrage en l'ajoutant à votre commande de démarrage :
```
python manage.py migrate && gunicorn fapag_collecte_backend.wsgi:application
```

### Erreurs de fichiers statiques
Vérifiez que `whitenoise` est correctement configuré dans `settings.py` et que `collectstatic` est exécuté pendant le déploiement.

### Problèmes de connexion à la base de données
Vérifiez que la variable `DATABASE_URL` est correctement définie et que la base de données est accessible depuis l'application.
