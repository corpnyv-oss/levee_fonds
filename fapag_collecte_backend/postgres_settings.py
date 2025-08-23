import os
from pathlib import Path
from .settings import *

# Configuration PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'levee_fonds',
        'USER': 'postgres',
        'PASSWORD': 'Root@FAPAG@2025',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Configuration pour éviter l'erreur SINGPAY_ALLOWED_IPS
SINGPAY_ALLOWED_IPS = os.environ.get('SINGPAY_ALLOWED_IPS', '').split(',') if os.environ.get('SINGPAY_ALLOWED_IPS') else []