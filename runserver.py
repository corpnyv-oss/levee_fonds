import os
import sys
from django.core.management.commands.runserver import Command as RunserverCommand
from django.core.servers.basehttp import WSGIServer

def run():
    # Désactiver la validation du host
    from django.http.request import validate_host
    def patched_validate_host(host, allowed_hosts):
        return True
    
    import django.core.handlers.wsgi
    django.core.handlers.wsgi.WSGIRequest.host = property(lambda self: 'localhost:8081')
    
    # Remplacer la fonction de validation
    import django.http.request
    django.http.request.validate_host = patched_validate_host
    
    # Lancer le serveur
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fapag_collecte_backend.settings')
    from django.core.management import execute_from_command_line
    
    # Désactiver le rechargement automatique pour éviter les problèmes
    sys.argv.append('--noreload')
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8081'])

if __name__ == '__main__':
    run()
