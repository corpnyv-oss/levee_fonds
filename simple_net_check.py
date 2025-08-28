import socket
import sys

def main():
    host = "aws-1-eu-west-3.pooler.supabase.com"
    port = 5432
    
    print(f"Tentative de connexion à {host}:{port}...")
    
    try:
        # Créer un socket TCP/IP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Définir un timeout de 10 secondes
        sock.settimeout(10)
        
        # Tenter de se connecter
        print(f"Connecté à {host}:{port}" if sock.connect_ex((host, port)) == 0 
              else f"Échec de la connexion à {host}:{port}")
        
        # Fermer la connexion
        sock.close()
        
    except socket.error as e:
        print(f"Erreur de socket: {e}")
    except Exception as e:
        print(f"Erreur inattendue: {e}")

if __name__ == "__main__":
    main()
