#!/bin/bash

# Afficher le répertoire de travail actuel
echo "Répertoire de travail actuel: $(pwd)"

# Afficher le contenu du répertoire
echo "Contenu du répertoire:"
ls -la

# Afficher la version de Python
echo "Version de Python:"
python --version

# Afficher la version de pip
echo "Version de pip:"
pip --version

# Afficher les variables d'environnement
echo "Variables d'environnement:
$(env | sort)"

# Vérifier si le fichier wsgi.py existe
if [ -f "fapag_collecte_backend/wsgi.py" ]; then
    echo "Le fichier wsgi.py existe bien"
else
    echo "ERREUR: Le fichier wsgi.py est introuvable"
    exit 1
fi

# Lancer Gunicorn avec plus de logs
echo "Démarrage de Gunicorn..."
cd /opt/render/project/src
python -m gunicorn fapag_collecte_backend.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 4 \
    --timeout 120 \
    --log-level debug \
    --access-logfile - \
    --error-logfile -
