@echo off
echo === Configuration de l'environnement ===

:: Vérifier Python
python --version
if %errorlevel% neq 0 (
    echo Erreur: Python n'est pas accessible
    pause
    exit /b 1
)

echo.
echo === Installation des dépendances ===
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Erreur lors de l'installation des dépendances
    pause
    exit /b 1
)

echo.
echo === Création des migrations ===
python manage.py makemigrations
if %errorlevel% neq 0 (
    echo Erreur lors de la création des migrations
    pause
    exit /b 1
)

echo.
echo === Application des migrations ===
python manage.py migrate
if %errorlevel% neq 0 (
    echo Erreur lors de l'application des migrations
    pause
    exit /b 1
)

echo.
echo === Création du superutilisateur ===
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fapag_collecte_backend.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superutilisateur créé avec succès!')
else:
    print('Le superutilisateur existe déjà')
"

echo.
echo === Démarrage du serveur de développement ===
python manage.py runserver

pause
