#!/usr/bin/env python3
"""
Test simple de l'API FAPAG
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("🧪 TEST SIMPLE DE L'API FAPAG")
    print("=" * 40)
    
    # Test 1: Vérifier que l'API répond
    try:
        response = requests.get(f"{BASE_URL}/api/", timeout=10)
        print(f"✅ API accessible: {response.status_code}")
        if response.status_code == 401:
            print("   → 401 est normal (authentification requise)")
        print(f"   → Réponse: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ API inaccessible: {e}")
        return False
    
    # Test 2: Vérifier Swagger
    try:
        response = requests.get(f"{BASE_URL}/swagger/", timeout=10)
        print(f"✅ Swagger accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Swagger inaccessible: {e}")
    
    # Test 3: Vérifier la page d'accueil
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        print(f"✅ Page d'accueil accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Page d'accueil inaccessible: {e}")
    
    print("\n" + "=" * 40)
    print("🏁 TEST TERMINÉ")
    print("\n📋 Résumé:")
    print(f"   🌐 URL API: {BASE_URL}/api/")
    print(f"   📚 URL Swagger: {BASE_URL}/swagger/")
    print(f"   🏠 URL Accueil: {BASE_URL}/")
    print("\n💡 Pour tester l'API:")
    print("   - Utilisez Postman ou curl")
    print("   - Utilisez HTTP (pas HTTPS)")
    print("   - L'erreur 401 est normale (auth requise)")
    
    return True

if __name__ == "__main__":
    test_api()
