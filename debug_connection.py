import sys
import socket
import ssl
import time

def test_connection(host, port, timeout=10):
    print(f"Tentative de connexion à {host}:{port} avec un délai de {timeout} secondes...")
    
    try:
        # Créer un socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        print(f"Connexion au socket...")
        start_time = time.time()
        sock.connect((host, port))
        end_time = time.time()
        
        print(f"✅ Connexion TCP réussie en {end_time - start_time:.2f} secondes")
        
        # Essayer une connexion SSL
        print("Tentative de connexion SSL...")
        context = ssl.create_default_context()
        ssl_sock = context.wrap_socket(sock, server_hostname=host)
        print("✅ Connexion SSL établie")
        
        # Lire la bannière du serveur
        banner = ssl_sock.recv(4096)
        print(f"Bannière du serveur: {banner.decode('utf-8', errors='ignore')}")
        
        ssl_sock.close()
        return True
        
    except socket.timeout:
        print(f"❌ Timeout de connexion après {timeout} secondes")
    except socket.gaierror as e:
        print(f"❌ Erreur de résolution d'adresse: {e}")
    except ssl.SSLError as e:
        print(f"❌ Erreur SSL: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
    
    return False

if __name__ == "__main__":
    host = "dpg-d2l2ir95pdvs73a92fog-a.frankfurt-postgres.render.com"
    port = 5432
    
    print(f"=== Test de connexion à {host}:{port} ===")
    
    # Tester la résolution DNS
    try:
        ip = socket.gethostbyname(host)
        print(f"✅ Résolution DNS réussie: {host} → {ip}")
    except socket.gaierror as e:
        print(f"❌ Échec de la résolution DNS: {e}")
        sys.exit(1)
    
    # Tester la connexion avec un délai plus long
    test_connection(host, port, timeout=15)
