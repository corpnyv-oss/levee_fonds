print("=== Test Python simple ===")
print("Si vous voyez ce message, Python fonctionne correctement.")

# Vérifier les imports essentiels
try:
    import sys
    import os
    print(f"\n=== Informations système ===")
    print(f"Python: {sys.version}")
    print(f"Exécutable: {sys.executable}")
    print(f"Répertoire de travail: {os.getcwd()}")
    print("\n✅ Les modules de base de Python fonctionnent correctement")
    
except Exception as e:
    print(f"\n❌ Erreur: {e}")
