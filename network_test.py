import socket
import sys

def test_connection(host, port):
    try:
        print(f"Tentative de connexion à {host}:{port}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        
        if result == 0:
            print(f"✅ Le port {port} est ouvert sur {host}")
            return True
        else:
            print(f"❌ Le port {port} est fermé ou inaccessible sur {host}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la tentative de connexion: {e}")
        return False
    finally:
        sock.close()

if __name__ == "__main__":
    host = "dpg-d2l2ir95pdvs73a92fog-a.frankfurt-postgres.render.com"
    port = 5432
    
    print(f"=== Test de connectivité réseau vers {host}:{port} ===")
    
    # Résolution DNS
    try:
        ip = socket.gethostbyname(host)
        print(f"Résolution DNS: {host} → {ip}")
    except Exception as e:
        print(f"❌ Erreur de résolution DNS pour {host}: {e}")
        sys.exit(1)
    
    # Test de connexion
    if test_connection(ip, port):
        print("\n✅ Le serveur est accessible. Le problème semble être lié à l'authentification ou à la configuration de la base de données.")
    else:
        print("\n❌ Le serveur n'est pas accessible. Vérifiez votre connexion Internet et les règles de pare-feu.")
