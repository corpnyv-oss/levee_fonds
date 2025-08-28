# Documentation de l'API FAPAG Collecte

## Authentification

### Obtenir un token JWT

```http
POST /api/auth/token/
```

**Corps de la requête (JSON):**
```json
{
    "username": "votre_email",
    "password": "votre_mot_de_passe"
}
```

**Réponse en cas de succès (200 OK):**
```json
{
    "refresh": "votre_refresh_token",
    "access": "votre_access_token"
}
```

### Rafraîchir un token

```http
POST /api/auth/token/refresh/
```

**Corps de la requête (JSON):**
```json
{
    "refresh": "votre_refresh_token"
}
```

## Cagnottes

### Lister toutes les cagnottes

```http
GET /api/cagnottes/
```

**Paramètres de requête:**
- `status` (optionnel): Filtrer par statut (active, terminee, en_attente, archivee)
- `ordering` (optionnel): Trier les résultats (ex: `-date_creation`)

### Créer une cagnotte

```http
POST /api/cagnottes/
```

**En-têtes requis:**
- `Authorization: Bearer <access_token>`
- `Content-Type: multipart/form-data`

**Corps de la requête (form-data):**
- `titre` (obligatoire): Titre de la cagnotte
- `description` (obligatoire): Description détaillée
- `objectif` (obligatoire): Montant objectif (nombre décimal)
- `image` (optionnel): Image de la cagnotte
- `date_debut` (obligatoire): Date de début (format: YYYY-MM-DD)
- `date_fin` (obligatoire): Date de fin (format: YYYY-MM-DD)

## Participations

### Participer à une cagnotte

```http
POST /api/participations/
```

**En-têtes requis:**
- `Authorization: Bearer <access_token>`
- `Content-Type: application/json`

**Corps de la requête (JSON):**
```json
{
    "cagnotte": 1,
    "montant": 50.00,
    "message": "Message de soutien (optionnel)"
}
```

### Initialiser un paiement via SingPay

```http
POST /api/participations/{id}/init-singpay/
```

**En-têtes requis:**
- `Authorization: Bearer <access_token>`

## Transactions

### Suivre une transaction

```http
GET /api/transactions/{id}/
```

**En-têtes requis:**
- `Authorization: Bearer <access_token>`

## Actualités

### Voir les actualités d'une cagnotte

```http
GET /api/actualites/?cagnotte={cagnotte_id}
```

## Gestion du compte

### S'inscrire

```http
POST /api/auth/register/
```

**Corps de la requête (JSON):**
```json
{
    "email": "utilisateur@example.com",
    "password": "mot_de_passe_securise",
    "password2": "mot_de_passe_securise",
    "first_name": "Prénom",
    "last_name": "Nom"
}
```

### Activer l'authentification à deux facteurs

1. **Démarrer la configuration 2FA**
   ```http
   GET /account/two_factor/setup/
   ```

2. **Configurer l'authentification par application**
   ```http
   POST /account/two_factor/setup/
   ```
   
   Suivre les instructions pour scanner le QR code avec une application d'authentification.

## Gestion des erreurs

L'API renvoie les codes d'erreur HTTP standard avec un corps de réponse au format JSON contenant les détails de l'erreur.

**Exemple d'erreur 400:**
```json
{
    "detail": "Invalid input.",
    "errors": {
        "champ": ["Message d'erreur spécifique au champ"]
    }
}
```

**Codes d'erreur courants:**
- 400: Requête mal formée ou données invalides
- 401: Non authentifié
- 403: Accès refusé
- 404: Ressource non trouvée
- 429: Trop de requêtes (rate limiting)
- 500: Erreur serveur
