#!/bin/bash

API_URL="http://127.0.0.1:8000/api"

# Identifiants à adapter
CLIENT_EMAIL="client@email.com"
CLIENT_PASSWORD="motdepasseclient"
ADMIN_EMAIL="bobo@email.com"
ADMIN_PASSWORD="yvan2004"

echo "=== TESTS PARTICIPATION (création, modification, suppression) ==="
# Création d'une participation (admin)
PARTICIPATION_ID=$(curl -s -X POST $API_URL/participations/ -H "Authorization: Bearer $ADMIN_TOKEN" -H "Content-Type: application/json" -d '{"utilisateur": 2, "cagnotte": 1, "montant": 100, "statut": "en_attente", "reference": "refadmin1"}' | python -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "Participation créée avec ID: $PARTICIPATION_ID"

# Modification (PATCH) par admin
curl -i -X PATCH $API_URL/participations/$PARTICIPATION_ID/ -H "Authorization: Bearer $ADMIN_TOKEN" -H "Content-Type: application/json" -d '{"statut": "validee"}'
echo

# Suppression par admin
curl -i -X DELETE $API_URL/participations/$PARTICIPATION_ID/ -H "Authorization: Bearer $ADMIN_TOKEN"
echo

# Tentative de suppression par client (doit échouer)
curl -i -X DELETE $API_URL/participations/$PARTICIPATION_ID/ -H "Authorization: Bearer $CLIENT_TOKEN"
echo

echo "=== TESTS TRANSACTION (lecture, modification, suppression) ==="
# Lecture (GET) par client
curl -i $API_URL/transactions/ -H "Authorization: Bearer $CLIENT_TOKEN"
echo

# Modification (PATCH) par admin (adapte l'ID)
# curl -i -X PATCH $API_URL/transactions/1/ -H "Authorization: Bearer $ADMIN_TOKEN" -H "Content-Type: application/json" -d '{"statut": "reussie"}'
# echo

# Suppression par admin (adapte l'ID)
# curl -i -X DELETE $API_URL/transactions/1/ -H "Authorization: Bearer $ADMIN_TOKEN"
# echo

# Tentative de suppression par client (doit échouer)
# curl -i -X DELETE $API_URL/transactions/1/ -H "Authorization: Bearer $CLIENT_TOKEN"
# echo
# Obtenir les tokens
CLIENT_TOKEN=$(curl -s -X POST $API_URL/auth/token/ -H "Content-Type: application/json" -d "{\"email\": \"$CLIENT_EMAIL\", \"password\": \"$CLIENT_PASSWORD\"}" | jq -r .access)
ADMIN_TOKEN=$(curl -s -X POST $API_URL/auth/token/ -H "Content-Type: application/json" -d "{\"email\": \"$ADMIN_EMAIL\", \"password\": \"$ADMIN_PASSWORD\"}" | jq -r .access)

echo "=== TESTS NON AUTHENTIFIÉ ==="
curl -i $API_URL/cagnottes/
echo
curl -i -X POST $API_URL/cagnottes/ -H "Content-Type: application/json" -d '{"titre": "Test", "description": "desc", "objectif": 1000, "date_debut": "2025-08-18", "date_fin": "2025-09-18"}'
echo

echo "=== TESTS CLIENT AUTHENTIFIÉ ==="
curl -i $API_URL/cagnottes/ -H "Authorization: Bearer $CLIENT_TOKEN"
echo
curl -i -X POST $API_URL/cagnottes/ -H "Authorization: Bearer $CLIENT_TOKEN" -H "Content-Type: application/json" -d '{"titre": "Test Client", "description": "desc", "objectif": 1000, "date_debut": "2025-08-18", "date_fin": "2025-09-18"}'
echo

echo "=== TESTS ADMIN AUTHENTIFIÉ ==="
curl -i $API_URL/cagnottes/ -H "Authorization: Bearer $ADMIN_TOKEN"
echo
curl -i -X POST $API_URL/cagnottes/ -H "Authorization: Bearer $ADMIN_TOKEN" -H "Content-Type: application/json" -d '{"titre": "Test Admin", "description": "desc", "objectif": 1000, "date_debut": "2025-08-18", "date_fin": "2025-09-18"}'
echo

echo "=== TEST ENDPOINT STRICTEMENT ADMIN (UTILISATEURS) ==="
curl -i $API_URL/utilisateurs/ -H "Authorization: Bearer $CLIENT_TOKEN"
echo
curl -i $API_URL/utilisateurs/ -H "Authorization: Bearer $ADMIN_TOKEN"
echo


# Pour tester la suppression, adapte l'ID à une participation existante
# curl -i -X DELETE $API_URL/participations/1/ -H "Authorization: Bearer $CLIENT_TOKEN"
# curl -i -X DELETE $API_URL/participations/1/ -H "Authorization: Bearer $ADMIN_TOKEN"