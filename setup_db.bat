@echo off
echo Configuration de la base de données...

REM Vérifier les dépendances
pip install psycopg2-binary django-db-geventpool

REM Tester la connexion à la base de données
echo Test de connexion à la base de données...
python -c "import psycopg2; conn = psycopg2.connect(dbname='levee_fonds', user='postgres', password='Root@FAPAG@2025', host='localhost', port='5432'); print('✅ Connexion réussie!'); conn.close()"

REM Configurer les variables d'environnement
echo Configuration des variables d'environnement...
set DJANGO_SETTINGS_MODULE=temp_db_settings
set DEBUG=True

REM Effectuer les migrations
echo Application des migrations...
python manage.py makemigrations
python manage.py migrate

REM Créer un superutilisateur
echo Création d'un superutilisateur...
python manage.py createsuperuser --username=admin --email=admin@example.com --noinput

echo Configuration terminée !
echo Pour démarrer le serveur, exécutez :
echo python manage.py runserver
