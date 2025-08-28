import os
from celery import Celery
from django.conf import settings

# Définir le module de paramètres par défaut pour l'application Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fapag_collecte_backend.settings')

app = Celery('fapag_collecte_backend')

# Utiliser une chaîne ici pour que le worker n'ait pas à sérialiser
# l'objet de configuration pour les processus enfants.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Charger les tâches depuis toutes les applications Django enregistrées
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Configuration pour les tâches périodiques (optionnel)
app.conf.beat_schedule = {}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
