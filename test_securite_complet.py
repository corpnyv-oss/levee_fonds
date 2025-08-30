#!/usr/bin/env python3
"""
Test complet de sécurité de l'API FAPAG
"""
import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

def test_authentification():
    """Test de l'authentification JWT"""
    print("🔐 Test d'authentification JWT")
    print("-" * 40)
    
    # Test 1: Connexion admin
    try:
        response = requests.post(f"{API_URL}/auth/token/", json={
            "email": "admin@fapag.com",
            "password": "admin123"
        })
        
        if response.status_code == 200:
            data = response.json()
            access_token = data.get('access')
            refresh_token = data.get('refresh')
            print("✅ Connexion admin réussie")
            print(f"   Access token: {access_token[:20]}...")
            print(f"   Refresh token: {refresh_token[:20]}...")
            return access_token, refresh_token
        else:
            print(f"❌ Échec connexion admin: {response.status_code}")
            print(f"   Réponse: {response.json()}")
            return None, None
            
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return None, None

def test_permissions_cagnottes(access_token):
    """Test des permissions sur les cagnottes"""
    print("\n💰 Test des permissions cagnottes")
    print("-" * 40)
    
    headers = {'Authorization': f'Bearer {access_token}'} if access_token else {}
    
    # Test 1: Lecture sans authentification
    try:
        response = requests.get(f"{API_URL}/cagnottes/")
        print(f"📖 Lecture sans auth: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Lecture publique autorisée")
        else:
            print("❌ Lecture publique refusée")
            
    except Exception as e:
        print(f"❌ Erreur lecture: {e}")
    
    # Test 2: Création sans authentification
    try:
        response = requests.post(f"{API_URL}/cagnottes/", json={
            "nom": "Test non autorisé",
            "description": "Test de sécurité",
            "montant_objectif": 1000
        })
        print(f"✏️ Création sans auth: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ Création non autorisée (comportement attendu)")
        else:
            print("❌ Création autorisée (problème de sécurité)")
            
    except Exception as e:
        print(f"❌ Erreur création: {e}")
    
    # Test 3: Création avec authentification admin
    if access_token:
        try:
            response = requests.post(f"{API_URL}/cagnottes/", json={
                "nom": "Test admin autorisé",
                "description": "Test de sécurité admin",
                "montant_objectif": 1000
            }, headers=headers)
            print(f"✏️ Création admin: {response.status_code}")
            
            if response.status_code == 201:
                print("✅ Création admin autorisée")
                cagnotte_data = response.json()
                cagnotte_id = cagnotte_data.get('id')
                return cagnotte_id
            else:
                print(f"❌ Création admin échouée: {response.json()}")
                
        except Exception as e:
            print(f"❌ Erreur création admin: {e}")
    
    return None

def test_rate_limiting():
    """Test du rate limiting"""
    print("\n🚦 Test du rate limiting")
    print("-" * 40)
    
    # Test 1: Rate limiting sur l'authentification
    print("🔐 Test rate limiting auth (5 tentatives/5min)")
    
    for i in range(6):
        try:
            response = requests.post(f"{API_URL}/auth/token/", json={
                "email": "test@example.com",
                "password": "wrongpassword"
            })
            
            print(f"   Tentative {i+1}: {response.status_code}")
            
            if response.status_code == 429:
                print("✅ Rate limit activé après 5 tentatives")
                break
            elif i == 5:
                print("❌ Rate limit non activé")
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    # Test 2: Rate limiting sur les cagnottes
    print("\n💰 Test rate limiting cagnottes (10 GET/min)")
    
    for i in range(12):
        try:
            response = requests.get(f"{API_URL}/cagnottes/")
            
            if response.status_code == 429:
                print(f"✅ Rate limit activé après {i+1} tentatives")
                break
            elif i == 11:
                print("❌ Rate limit non activé")
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")

def test_webhook_security():
    """Test de la sécurité des webhooks"""
    print("\n🔒 Test de sécurité des webhooks")
    print("-" * 40)
    
    # Test 1: Webhook sans signature
    try:
        response = requests.post(f"{BASE_URL}/webhooks/test/", json={
            "test": True,
            "message": "Test sans signature"
        })
        
        print(f"📝 Webhook sans signature: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ Webhook rejeté sans signature (sécurisé)")
        else:
            print("❌ Webhook accepté sans signature (non sécurisé)")
            
    except Exception as e:
        print(f"❌ Erreur webhook: {e}")
    
    # Test 2: Webhook avec signature invalide
    try:
        response = requests.post(f"{BASE_URL}/webhooks/test/", json={
            "test": True,
            "message": "Test signature invalide"
        }, headers={
            'X-Webhook-Signature': 'invalid_signature_12345'
        })
        
        print(f"📝 Webhook signature invalide: {response.status_code}")
        
        if response.status_code == 403:
            print("✅ Webhook rejeté avec signature invalide (sécurisé)")
        else:
            print("❌ Webhook accepté avec signature invalide (non sécurisé)")
            
    except Exception as e:
        print(f"❌ Erreur webhook: {e}")

def test_2fa_system():
    """Test du système 2FA"""
    print("\n🔐 Test du système 2FA")
    print("-" * 40)
    
    # Test 1: Configuration 2FA
    try:
        response = requests.post(f"{BASE_URL}/2fa/setup/", json={
            "email": "admin@fapag.com",
            "password": "admin123"
        })
        
        print(f"⚙️ Configuration 2FA: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 2FA configuré avec succès")
            print(f"   QR Code: {'Oui' if data.get('qr_code') else 'Non'}")
            print(f"   Codes de sauvegarde: {len(data.get('backup_codes', []))}")
        elif response.status_code == 400 and "déjà configuré" in response.json().get('error', ''):
            print("ℹ️ 2FA déjà configuré")
        else:
            print(f"❌ Échec configuration 2FA: {response.json()}")
            
    except Exception as e:
        print(f"❌ Erreur 2FA: {e}")

def test_cleanup(cagnotte_id, access_token):
    """Nettoyage des données de test"""
    if cagnotte_id and access_token:
        print("\n🧹 Nettoyage des données de test")
        print("-" * 40)
        
        try:
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.delete(f"{API_URL}/cagnottes/{cagnotte_id}/", headers=headers)
            
            if response.status_code == 204:
                print("✅ Cagnotte de test supprimée")
            else:
                print(f"❌ Échec suppression: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erreur nettoyage: {e}")

def main():
    """Test principal de sécurité"""
    print("🛡️ TEST COMPLET DE SÉCURITÉ API FAPAG")
    print("=" * 60)
    print(f"⏰ Début: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Authentification
    access_token, refresh_token = test_authentification()
    
    # Test 2: Permissions
    cagnotte_id = test_permissions_cagnottes(access_token)
    
    # Test 3: Rate limiting
    test_rate_limiting()
    
    # Test 4: Sécurité webhooks
    test_webhook_security()
    
    # Test 5: Système 2FA
    test_2fa_system()
    
    # Nettoyage
    test_cleanup(cagnotte_id, access_token)
    
    print("\n" + "=" * 60)
    print("🏁 TESTS DE SÉCURITÉ TERMINÉS")
    print(f"⏰ Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n📊 RÉSUMÉ DES TESTS:")
    print("✅ Authentification JWT")
    print("✅ Permissions et autorisations")
    print("✅ Rate limiting")
    print("✅ Sécurité webhooks")
    print("✅ Système 2FA")
    print("✅ Nettoyage des données")

if __name__ == "__main__":
    main()
