#!/usr/bin/env python3
"""
Script de test pour le système 2FA
"""
import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000"
ADMIN_EMAIL = "admin@fapag.com"  # Remplacer par un vrai admin
ADMIN_PASSWORD = "admin123"       # Remplacer par le vrai mot de passe

def test_2fa_system():
    """Teste le système 2FA complet"""
    
    print("🔐 Test du système 2FA")
    print("=" * 50)
    
    # Test 1: Configuration 2FA
    print("\n1️⃣ Test: Configuration 2FA")
    print("   Configuration de la 2FA pour un administrateur")
    
    try:
        response = requests.post(f"{BASE_URL}/2fa/setup/", json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        })
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ SUCCÈS: 2FA configuré")
            print(f"   QR Code généré: {'Oui' if data.get('qr_code') else 'Non'}")
            print(f"   Clé secrète: {data.get('secret_key', 'Non générée')}")
            print(f"   Codes de sauvegarde: {len(data.get('backup_codes', []))} générés")
            
            # Sauvegarder les données pour les tests suivants
            secret_key = data.get('secret_key')
            backup_codes = data.get('backup_codes', [])
            qr_code = data.get('qr_code')
            
        elif response.status_code == 400 and "déjà configuré" in response.json().get('error', ''):
            print("   ℹ️ INFO: 2FA déjà configuré pour cet utilisateur")
            secret_key = "existing_key"
            backup_codes = ["12345678", "87654321"]  # Codes fictifs pour le test
            qr_code = "existing_qr"
            
        else:
            print(f"   ❌ ÉCHEC: {response.json()}")
            return
            
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
        return
    
    # Test 2: Vérification de la configuration 2FA
    print("\n2️⃣ Test: Vérification de la configuration 2FA")
    print("   Confirmation de la configuration avec un token TOTP")
    
    # Simuler un token TOTP (en réalité, il faudrait le générer avec pyotp)
    test_token = "123456"  # Token fictif pour le test
    
    try:
        response = requests.post(f"{BASE_URL}/2fa/verify-setup/", json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD,
            "token": test_token
        })
        
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.json()}")
        
        if response.status_code == 200:
            print("   ✅ SUCCÈS: Configuration 2FA confirmée")
        elif response.status_code == 400 and "Token 2FA invalide" in response.json().get('error', ''):
            print("   ℹ️ INFO: Token invalide (comportement attendu avec un token fictif)")
        else:
            print("   ❌ ÉCHEC: Problème lors de la confirmation")
            
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
    
    # Test 3: Connexion avec 2FA
    print("\n3️⃣ Test: Connexion avec 2FA")
    print("   Tentative de connexion avec authentification 2FA")
    
    try:
        response = requests.post(f"{BASE_URL}/2fa/login/", json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD,
            "token": test_token
        })
        
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.json()}")
        
        if response.status_code == 200:
            print("   ✅ SUCCÈS: Connexion 2FA réussie")
        elif response.status_code == 400 and "Token 2FA invalide" in response.json().get('error', ''):
            print("   ℹ️ INFO: Token invalide (comportement attendu)")
        else:
            print("   ❌ ÉCHEC: Problème lors de la connexion 2FA")
            
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
    
    # Test 4: Connexion avec code de sauvegarde
    print("\n4️⃣ Test: Connexion avec code de sauvegarde")
    print("   Tentative de connexion avec un code de sauvegarde")
    
    if backup_codes:
        backup_code = backup_codes[0]
        
        try:
            response = requests.post(f"{BASE_URL}/2fa/backup/", json={
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD,
                "backup_code": backup_code
            })
            
            print(f"   Status: {response.status_code}")
            print(f"   Réponse: {response.json()}")
            
            if response.status_code == 200:
                print("   ✅ SUCCÈS: Connexion avec code de sauvegarde réussie")
            elif response.status_code == 400 and "Code de sauvegarde invalide" in response.json().get('error', ''):
                print("   ℹ️ INFO: Code de sauvegarde invalide (peut-être déjà utilisé)")
            else:
                print("   ❌ ÉCHEC: Problème lors de la connexion avec code de sauvegarde")
                
        except Exception as e:
            print(f"   ❌ ERREUR: {e}")
    else:
        print("   ⚠️ SKIP: Aucun code de sauvegarde disponible")
    
    # Test 5: Statut 2FA
    print("\n5️⃣ Test: Vérification du statut 2FA")
    print("   Récupération du statut 2FA de l'utilisateur")
    
    try:
        # D'abord se connecter pour obtenir une session
        login_response = requests.post(f"{BASE_URL}/2fa/login/", json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD,
            "token": test_token
        })
        
        if login_response.status_code == 200:
            # Utiliser la session pour vérifier le statut
            session = requests.Session()
            session.cookies.update(login_response.cookies)
            
            status_response = session.get(f"{BASE_URL}/2fa/status/")
            
            print(f"   Status: {status_response.status_code}")
            print(f"   Réponse: {status_response.json()}")
            
            if status_response.status_code == 200:
                print("   ✅ SUCCÈS: Statut 2FA récupéré")
            else:
                print("   ❌ ÉCHEC: Impossible de récupérer le statut 2FA")
        else:
            print("   ⚠️ SKIP: Impossible de se connecter pour tester le statut")
            
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Tests 2FA terminés")
    print("\n📝 Notes importantes:")
    print("   - Les tokens TOTP sont générés par Google Authenticator")
    print("   - Pour tester complètement, configurez un vrai appareil TOTP")
    print("   - Les codes de sauvegarde sont à usage unique")
    print("   - La 2FA est obligatoire pour les administrateurs uniquement")

if __name__ == "__main__":
    test_2fa_system()
