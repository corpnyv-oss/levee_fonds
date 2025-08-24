@echo off
echo Création d'un nouvel environnement virtuel...
rmdir /s /q venv
python -m venv venv

call venv\Scripts\activate.bat

echo Installation des dépendances...
pip install --upgrade pip
pip install -r requirements.txt

echo Vérification de l'installation...
python -c "import django; print(f'Django version: {django.__version__}')"
python -c "import psycopg2; print(f'psycopg2 version: {psycopg2.__version__} if hasattr(psycopg2, '__version__') else 'psycopg2 importé avec succès')"

echo.
echo Environnement virtuel configuré avec succès !
pause
