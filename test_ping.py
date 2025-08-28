import socket
import sys

def test_connection(host, port):
    try:
        # Créer un socket TCP/IP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # Timeout de 5 secondes
        
        print(f"Tentative de connexion à {host}:{port}...")
        
        # Tester la connexion
        result = sock.connect_ex((host, port))
        
        if result == 0:
            print(f"✅ Le port {port} est ouvert sur {host}")
            return True
        else:
            print(f"❌ Le port {port} est fermé ou inaccessible sur {host} (code: {result})")
            return False
            
    except socket.gaierror:
        print("❌ Erreur: Impossible de résoudre le nom d'hôte")
        return False
    except socket.timeout:
        print("❌ Erreur: Délai d'attente dépassé")
        return False
    except socket.error as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    finally:
        sock.close()

if __name__ == "__main__":
    host = "dpg-d2l2ir95pdvs73a92fog-a.oregon-postgres.render.com"
    port = 5432
    
    print(f"=== Test de connectivité à {host}:{port} ===\n")
    
    if not test_connection(host, port):
        print("\nSuggestions de dépannage:")
        print("1. Vérifiez votre connexion Internet")
        print("2. Vérifiez si le pare-feu bloque le port 5432")
        print("3. Vérifiez si le serveur PostgreSQL est en cours d'exécution")
        print("4. Vérifiez les paramètres de sécurité du serveur PostgreSQL")
        print("5. Contactez votre administrateur système ou l'hébergeur de la base de données")
