# Wrapper to provide a clean module path and explicit app_name for two_factor URLs
# This avoids tuple/list forms that can confuse Django's URL checks.

from two_factor.urls import urlpatterns as two_factor_urlpatterns

app_name = 'two_factor'
# Certains packages tiers peuvent insérer un préfixe de type chaîne en tête
# de urlpatterns (héritage anciennes versions). Django 5 lève urls.E004.
# On filtre donc toute entrée qui serait une chaîne.
urlpatterns = [p for p in two_factor_urlpatterns if not isinstance(p, str)]
