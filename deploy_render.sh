#!/bin/bash

# 🚀 Script de déploiement Render - API FAPAG
# Usage: ./deploy_render.sh

set -e  # Arrêter en cas d'erreur

echo "🛡️ DÉPLOIEMENT RENDER - API FAPAG"
echo "=================================="

# 1. Vérifications pré-déploiement
echo "🔍 Vérifications pré-déploiement..."

# Vérifier que Git est à jour
if [[ -n $(git status --porcelain) ]]; then
    echo "❌ ERREUR: Des modifications non commitées existent"
    git status
    exit 1
fi

# Vérifier que les tests passent
echo "🧪 Exécution des tests de sécurité..."
python test_securite_complet.py

# Vérifier la configuration Django
echo "⚙️ Vérification de la configuration Django..."
python manage.py check --deploy

# 2. Préparation du déploiement
echo "📦 Préparation du déploiement..."

# Créer un tag de version
VERSION=$(date +%Y%m%d_%H%M%S)
git tag "v$VERSION"
echo "🏷️ Tag créé: v$VERSION"

# 3. Déploiement sur Render
echo "🚀 Déploiement sur Render..."

# Pousser le code et les tags
git push origin main
git push origin --tags

echo "✅ Code poussé vers Render"

# 4. Vérification post-déploiement
echo "🔍 Vérification post-déploiement..."

# Attendre que le déploiement soit terminé
echo "⏳ Attente du déploiement..."
sleep 60

# URL de l'API (à adapter selon votre configuration)
API_URL="https://fapag-collecte-api.onrender.com"

# Test de santé de l'API
echo "🏥 Test de santé de l'API..."
if curl -f "$API_URL/healthz/" > /dev/null 2>&1; then
    echo "✅ API accessible"
else
    echo "❌ API non accessible"
    exit 1
fi

# Test de sécurité post-déploiement
echo "🛡️ Test de sécurité post-déploiement..."
python test_securite_complet.py --production-url "$API_URL"

# 5. Finalisation
echo "🎉 DÉPLOIEMENT TERMINÉ AVEC SUCCÈS !"
echo "📱 URL de l'API: $API_URL"
echo "📚 Documentation: $API_URL/swagger/"
echo "🔐 Admin: $API_URL/admin/"

# 6. Nettoyage
echo "🧹 Nettoyage..."
# Supprimer le tag local
git tag -d "v$VERSION"

echo "✅ Déploiement terminé !"
