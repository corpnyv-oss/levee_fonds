#!/usr/bin/env python3
"""
Script de test pour la sécurité des webhooks
"""
import hmac
import hashlib
import json
import time
import requests
from datetime import datetime, timezone

# Configuration
WEBHOOK_URL = "http://127.0.0.1:8000/webhooks/test/"
SECRET_KEY = "change-this-in-production"  # Doit correspondre à WEBHOOK_SECRET_KEY

def generate_hmac_signature(payload: bytes, secret_key: str) -> str:
    """Génère une signature HMAC pour le payload"""
    return hmac.new(
        secret_key.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

def test_webhook_security():
    """Teste la sécurité des webhooks"""
    
    print("🔒 Test de sécurité des webhooks")
    print("=" * 50)
    
    # Test 1: Webhook avec signature valide
    print("\n1️⃣ Test: Webhook avec signature HMAC valide")
    payload = {
        "test": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": "Test de sécurité webhook"
    }
    
    payload_bytes = json.dumps(payload).encode('utf-8')
    signature = generate_hmac_signature(payload_bytes, SECRET_KEY)
    
    headers = {
        'Content-Type': 'application/json',
        'X-Webhook-Signature': signature,
        'X-Webhook-Timestamp': datetime.now(timezone.utc).isoformat()
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.json()}")
        
        if response.status_code == 200:
            print("   ✅ SUCCÈS: Webhook accepté avec signature valide")
        else:
            print("   ❌ ÉCHEC: Webhook rejeté malgré signature valide")
            
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
    
    # Test 2: Webhook sans signature
    print("\n2️⃣ Test: Webhook sans signature HMAC")
    headers_no_sig = {
        'Content-Type': 'application/json',
        'X-Webhook-Timestamp': datetime.now(timezone.utc).isoformat()
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers_no_sig)
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.json()}")
        
        if response.status_code == 401:
            print("   ✅ SUCCÈS: Webhook rejeté sans signature")
        else:
            print("   ❌ ÉCHEC: Webhook accepté sans signature")
            
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
    
    # Test 3: Webhook avec signature invalide
    print("\n3️⃣ Test: Webhook avec signature HMAC invalide")
    invalid_signature = "invalid_signature_12345"
    
    headers_invalid = {
        'Content-Type': 'application/json',
        'X-Webhook-Signature': invalid_signature,
        'X-Webhook-Timestamp': datetime.now(timezone.utc).isoformat()
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers_invalid)
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.json()}")
        
        if response.status_code == 403:
            print("   ✅ SUCCÈS: Webhook rejeté avec signature invalide")
        else:
            print("   ❌ ÉCHEC: Webhook accepté avec signature invalide")
            
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
    
    # Test 4: Webhook avec horodatage ancien
    print("\n4️⃣ Test: Webhook avec horodatage ancien (> 5 minutes)")
    old_timestamp = datetime.now(timezone.utc).replace(year=2020).isoformat()
    
    headers_old = {
        'Content-Type': 'application/json',
        'X-Webhook-Signature': signature,
        'X-Webhook-Timestamp': old_timestamp
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers_old)
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.json()}")
        
        if response.status_code == 403:
            print("   ✅ SUCCÈS: Webhook rejeté avec horodatage ancien")
        else:
            print("   ❌ ÉCHEC: Webhook accepté avec horodatage ancien")
            
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Tests terminés")

if __name__ == "__main__":
    test_webhook_security()
