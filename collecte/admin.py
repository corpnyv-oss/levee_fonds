from django.contrib import admin
from .models import Cagnotte, Participation, Transaction, WebhookEvent, Actualite, Utilisateur

admin.site.register(Cagnotte)
admin.site.register(Participation)
admin.site.register(Transaction)
admin.site.register(WebhookEvent)
admin.site.register(Actualite)
admin.site.register(Utilisateur)
