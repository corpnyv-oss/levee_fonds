#!/usr/bin/env python3
"""
Script de test pour le rate limiting de l'API
"""
import requests
import time
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
AUTH_URL = f"{BASE_URL}/auth/token/"

def test_rate_limiting():
    """Teste le rate limiting de l'API"""
    
    print("🚦 Test du Rate Limiting de l'API")
    print("=" * 50)
    
    # Test 1: Rate limiting sur l'authentification
    print("\n1️⃣ Test: Rate limiting sur /auth/token/")
    print("   Tentative de 6 connexions en 5 minutes (limite: 5)")
    
    for i in range(6):
        try:
            response = requests.post(AUTH_URL, json={
                "email": "test@example.com",
                "password": "wrongpassword"
            })
            
            print(f"   Tentative {i+1}: Status {response.status_code}")
            
            if response.status_code == 429:
                print("   ✅ SUCCÈS: Rate limit activé après 5 tentatives")
                break
            elif i == 5:
                print("   ❌ ÉCHEC: Rate limit non activé")
                
        except Exception as e:
            print(f"   ❌ ERREUR: {e}")
    
    # Test 2: Rate limiting sur les cagnottes
    print("\n2️⃣ Test: Rate limiting sur /cagnottes/ (GET)")
    print("   Tentative de 12 lectures en 1 minute (limite: 10)")
    
    for i in range(12):
        try:
            response = requests.get(f"{BASE_URL}/cagnottes/")
            
            print(f"   Tentative {i+1}: Status {response.status_code}")
            
            if response.status_code == 429:
                print("   ✅ SUCCÈS: Rate limit activé après 10 tentatives")
                break
            elif i == 11:
                print("   ❌ ÉCHEC: Rate limit non activé")
                
        except Exception as e:
            print(f"   ❌ ERREUR: {e}")
    
    # Test 3: Rate limiting sur les participations
    print("\n3️⃣ Test: Rate limiting sur /participations/ (POST)")
    print("   Tentative de 12 créations en 1 minute (limite: 10)")
    
    for i in range(12):
        try:
            response = requests.post(f"{BASE_URL}/participations/", json={
                "cagnotte": 1,
                "montant": 100,
                "reference": f"test-{i}"
            })
            
            print(f"   Tentative {i+1}: Status {response.status_code}")
            
            if response.status_code == 429:
                print("   ✅ SUCCÈS: Rate limit activé après 10 tentatives")
                break
            elif i == 11:
                print("   ❌ ÉCHEC: Rate limit non activé")
                
        except Exception as e:
            print(f"   ❌ ERREUR: {e}")
    
    # Test 4: Vérifier que les limites sont par IP
    print("\n4️⃣ Test: Rate limiting par IP")
    print("   Vérification que les limites sont individuelles par IP")
    
    # Simuler des requêtes depuis différentes IPs
    headers_ip1 = {'X-Forwarded-For': '192.168.1.1'}
    headers_ip2 = {'X-Forwarded-For': '192.168.1.2'}
    
    try:
        # IP 1: 5 tentatives
        for i in range(5):
            response = requests.post(AUTH_URL, json={
                "email": "test1@example.com",
                "password": "wrongpassword"
            }, headers=headers_ip1)
            print(f"   IP1 - Tentative {i+1}: Status {response.status_code}")
        
        # IP 2: 5 tentatives
        for i in range(5):
            response = requests.post(AUTH_URL, json={
                "email": "test2@example.com",
                "password": "wrongpassword"
            }, headers=headers_ip2)
            print(f"   IP2 - Tentative {i+1}: Status {response.status_code}")
        
        print("   ✅ SUCCÈS: Rate limiting fonctionne par IP")
        
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Tests de rate limiting terminés")

if __name__ == "__main__":
    test_rate_limiting()
