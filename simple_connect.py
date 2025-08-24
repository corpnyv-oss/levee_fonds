import socket
import ssl
import sys

def test_connection():
    host = 'dpg-d2l2ir95pdvs73a92fog-a.frankfurt-postgres.render.com'
    port = 5432
    
    print(f"Tentative de connexion à {host}:{port}...")
    
    try:
        # Créer une socket TCP/IP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)  # Timeout de 10 secondes
        
        print(f"Connexion TCP/IP établie")
        
        # Essayer de se connecter
        sock.connect((host, port))
        print(f"✅ Connexion TCP/IP réussie à {host}:{port}")
        
        # Essayer de négocier SSL
        context = ssl.create_default_context()
        ssl_sock = context.wrap_socket(sock, server_hostname=host)
        print("✅ Négociation SSL réussie")
        
        # Fermer la connexion
        ssl_sock.close()
        return True
        
    except socket.timeout:
        print("❌ Délai d'attente dépassé lors de la tentative de connexion")
    except socket.gaierror as e:
        print(f"❌ Erreur de résolution du nom d'hôte: {e}")
    except ConnectionRefusedError:
        print("❌ Connexion refusée par l'hôte distant")
    except ssl.SSLError as e:
        print(f"❌ Erreur SSL: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
    
    return False

if __name__ == "__main__":
    test_connection()
