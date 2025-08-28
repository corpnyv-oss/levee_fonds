from sshtunnel import SSHTunnelForwarder
import psycopg2
import time

def test_ssh_tunnel():
    print("=== Test de connexion via tunnel SSH ===\n")
    
    # Paramètres du serveur SSH (à remplacer par vos informations)
    ssh_host = 'votre-serveur-ssh.com'  # Remplacez par l'adresse de votre serveur SSH
    ssh_username = 'votre-utilisateur'   # Votre nom d'utilisateur SSH
    ssh_password = 'votre-mot-de-passe'  # Votre mot de passe SSH (ou utilisez une clé)
    
    # Paramètres de la base de données PostgreSQL distante
    db_host = 'dpg-d2l2ir95pdvs73a92fog-a.oregon-postgres.render.com'
    db_port = 5432
    db_name = 'db_levee_fonds'
    db_user = 'db_levee_fonds_user'
    db_password = '3gWX7NcyKeyLbVTGHBerEiU5d37LSBHA'
    
    # Port local pour le tunnel
    local_port = 5433
    
    try:
        print(f"Création du tunnel SSH vers {ssh_host}...")
        
        with SSHTunnelForwarder(
            (ssh_host, 22),
            ssh_username=ssh_username,
            ssh_password=ssh_password,
            remote_bind_address=(db_host, db_port),
            local_bind_address=('127.0.0.1', local_port)
        ) as tunnel:
            print(f"Tunnel SSH établi sur le port local {local_port}")
            
            # Attendre que le tunnel soit prêt
            time.sleep(1)
            
            # Paramètres de connexion à travers le tunnel
            conn_params = {
                'dbname': db_name,
                'user': db_user,
                'password': db_password,
                'host': '127.0.0.1',
                'port': local_port,
                'sslmode': 'disable'  # Désactiver SSL car le trafic est déjà sécurisé par SSH
            }
            
            print("\nTentative de connexion à la base de données via le tunnel...")
            
            # Établir la connexion à la base de données
            conn = psycopg2.connect(**conn_params)
            print("✅ Connexion à la base de données réussie via le tunnel SSH!")
            
            # Exécuter une requête de test
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"\nVersion de PostgreSQL: {version[0]}")
            
            # Fermer la connexion
            conn.close()
            print("\nConnexion fermée.")
    
    except Exception as e:
        print(f"\n❌ Erreur lors de la création du tunnel ou de la connexion à la base de données:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {str(e)}")
        
        # Suggestions de dépannage
        print("\nSuggestions de dépannage:")
        print("1. Vérifiez que le serveur SSH est accessible et que les identifiants sont corrects")
        print("2. Vérifiez que le serveur PostgreSQL est accessible depuis le serveur SSH")
        print("3. Vérifiez que le port local {local_port} est disponible")
        print("4. Vérifiez que les identifiants de la base de données sont corrects")

if __name__ == "__main__":
    test_ssh_tunnel()
