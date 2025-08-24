import socket
import ssl

def test_connection(host, port):
    try:
        # Créer un socket
        sock = socket.create_connection((host, port), timeout=5)
        print(f"✅ Connexion réussie à {host}:{port}")
        sock.close()
        return True
    except socket.timeout:
        print(f"❌ Timeout lors de la connexion à {host}:{port}")
    except socket.gaierror as e:
        print(f"❌ Erreur de résolution d'adresse pour {host}: {e}")
    except Exception as e:
        print(f"❌ Erreur de connexion à {host}:{port}: {e}")
    return False

# Tester la connexion au serveur DNS de Google
print("\nTest de connexion à Google DNS (8.8.8.8:53)...")
test_connection("8.8.8.8", 53)

# Tester la connexion au serveur PostgreSQL
print("\nTest de connexion au serveur PostgreSQL...")
test_connection("dpg-d2l2ir95pdvs73a92fog-a.frankfurt-postgres.render.com", 5432)
