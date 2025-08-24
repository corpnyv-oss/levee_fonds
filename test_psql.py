import subprocess
import sys

def test_psql():
    try:
        print("=== Test de connexion PostgreSQL ===")
        print("1. Vérification de l'installation de psql...")
        try:
            psql_version = subprocess.run(['psql', '--version'], 
                                       capture_output=True, 
                                       text=True)
            print(f"Version de psql: {psql_version.stdout.strip()}")
        except Exception as e:
            print(f"❌ psql n'est pas installé ou n'est pas dans le PATH: {e}")
            print("Veuillez installer PostgreSQL ou ajouter psql au PATH")
            return

        print("\n2. Test de connexion à la base de données...")
        cmd = (
            'psql '
            '"host=dpg-d2l2ir95pdvs73a92fog-a.frankfurt-postgres.render.com '
            'port=5432 '
            'dbname=db_levee_fonds '
            'user=db_levee_fonds_user "\
            'sslmode=require"'  # Note: L'échappement est important ici
        )
        
        env = {
            'PGPASSWORD': '3gWX7NcyKeyLbVTGHBerEiU5d37LSBHA',
            'PATH': os.environ.get('PATH', '')
        }
        
        print(f"\nCommande exécutée: {cmd}")
        print("Connexion en cours...")
        
        result = subprocess.run(
            cmd,
            shell=True,
            env=env,
            capture_output=True,
            text=True
        )
        
        print("\n=== Résultats ===")
        print(f"Code de sortie: {result.returncode}")
        
        if result.stdout:
            print("\nSortie standard:")
            print(result.stdout)
            
        if result.stderr:
            print("\nErreur standard:")
            print(result.stderr)
            
        if result.returncode == 0:
            print("✅ Connexion réussie!")
        else:
            print("❌ Échec de la connexion")
            
    except Exception as e:
        print(f"\n❌ Erreur lors de l'exécution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import os
    test_psql()
