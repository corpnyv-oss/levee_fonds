import socket
import sys

def test_connection(host, port):
    try:
        # Créer un socket TCP/IP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # Timeout de 5 secondes
        
        # Tester la connexion
        result = sock.connect_ex((host, port))
        
        if result == 0:
            print(f"✅ Connexion réussie à {host}:{port}")
            return True
        else:
            print(f"❌ Échec de la connexion à {host}:{port} (code: {result})")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la connexion à {host}:{port}: {e}")
        return False
    finally:
        sock.close()

# Tester la connexion à Google DNS
print("\nTest de connexion à Google DNS (8.8.8.8:53)...")
test_connection("8.8.8.8", 53)

# Tester la connexion au serveur PostgreSQL
print("\nTest de connexion au serveur PostgreSQL...")
test_connection("dpg-d2l2ir95pdvs73a92fog-a.oregon-postgres.render.com", 5432)
