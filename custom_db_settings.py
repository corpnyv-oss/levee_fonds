from fapag_collecte_backend.settings import *

# Configuration de la base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_levee_fonds',
        'USER': 'db_levee_fonds_user',
        'PASSWORD': '3gWX7NcyKeyLbVTGHBerEiU5d37LSBHA',
        'HOST': 'dpg-d2l2ir95pdvs73a92fog-a',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'connect_timeout': 5,
            'sslmode': 'require',
        },
    }
}
