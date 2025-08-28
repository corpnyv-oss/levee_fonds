import socket
import ssl
import time

def test_connection(host, port, use_ssl=False, timeout=5):
    try:
        start_time = time.time()
        
        # Créer un socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        print(f"\nTest de connexion à {host}:{port}...")
        
        # Tester la connexion TCP de base
        print(f"1. Tentative de connexion TCP...")
        sock.connect((host, port))
        print(f"   ✅ Connexion TCP réussie en {time.time() - start_time:.2f}s")
        
        # Si SSL est requis
        if use_ssl:
            print("2. Configuration SSL...")
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            ssl_sock = context.wrap_socket(sock, server_hostname=host)
            print("   ✅ Connexion SSL établie")
            ssl_sock.close()
        else:
            sock.close()
            
        print(f"\n✅ Test de connexion réussi pour {host}:{port}")
        return True
        
    except socket.timeout:
        print(f"❌ Timeout lors de la connexion à {host}:{port} (vérifiez votre pare-feu/routeur)")
    except socket.gaierror as e:
        print(f"❌ Erreur de résolution d'adresse pour {host}: {e}")
    except ssl.SSLError as e:
        print(f"❌ Erreur SSL: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
    
    return False

# Tester la connexion au serveur PostgreSQL
test_connection("aws-1-eu-west-3.pooler.supabase.com", 5432, use_ssl=True)

# Tester la connexion à un serveur Web connu (Google)
test_connection("google.com", 443, use_ssl=True)
