import socket
import sys

def main():
    host = "dpg-d2l2ir95pdvs73a92fog-a.oregon-postgres.render.com"
    port = 5432
    
    print(f"Tentative de connexion à {host}:{port}...")
    
    try:
        # Créer un socket TCP/IP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Définir un timeout de 10 secondes
        sock.settimeout(10)
        
        # Tenter de se connecter
        result = sock.connect_ex((host, port))
        
        if result == 0:
            print(f"✅ Connexion réussie à {host}:{port}")
        else:
            print(f"❌ Échec de la connexion. Code d'erreur: {result}")
        
        # Fermer la connexion
        sock.close()
        
    except socket.error as e:
        print(f"❌ Erreur de socket: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    main()
