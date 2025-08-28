import socket
import ssl
import sys

def test_connection(host, port):
    try:
        # Créer un socket TCP/IP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)  # Timeout de 10 secondes
        
        print(f"\n🔍 Test de connexion à {host}:{port}...")
        
        # Tester la connexion TCP simple
        print(f"🔄 Tentative de connexion TCP...")
        result = sock.connect_ex((host, port))
        
        if result == 0:
            print(f"✅ Connexion TCP réussie à {host}:{port}")
            
            # Essayer avec SSL
            try:
                print("\n🔒 Tentative de connexion SSL...")
                context = ssl.create_default_context()
                
                # Désactiver la vérification du certificat pour les tests
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                
                # Créer une connexion sécurisée
                secure_sock = context.wrap_socket(sock, server_hostname=host)
                print("✅ Connexion SSL établie avec succès!")
                secure_sock.close()
                return True
                
            except Exception as e:
                print(f"❌ Erreur lors de la connexion SSL: {str(e)}")
                return False
                
        else:
            print(f"❌ Échec de la connexion TCP. Code d'erreur: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la connexion: {str(e)}")
        return False
    finally:
        sock.close()

if __name__ == "__main__":
    host = "aws-1-eu-west-3.pooler.supabase.com"
    port = 5432
    
    print(f"=== Test de connectivité à Supabase ===\n")
    print(f"🌐 Hôte: {host}")
    print(f"🚪 Port: {port}")
    
    if not test_connection(host, port):
        print("\n🔧 Suggestions de dépannage:")
        print("1. Vérifiez votre connexion Internet")
        print("2. Vérifiez que le pare-feu autorise les connexions sortantes sur le port 5432")
        print("3. Essayez de désactiver temporairement votre antivirus/pare-feu")
        print("4. Vérifiez que votre fournisseur d'accès Internet ne bloque pas le port 5432")
        print("5. Essayez de vous connecter depuis un autre réseau (par exemple, un hotspot mobile)")
