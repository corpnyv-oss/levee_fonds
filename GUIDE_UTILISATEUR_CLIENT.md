# 👤 Guide Utilisateur Client - API FAPAG

## 📋 Table des matières
1. [Première connexion](#première-connexion)
2. [Utilisation quotidienne](#utilisation-quotidienne)
3. [Sécurité de votre compte](#sécurité-de-votre-compte)
4. [Support et assistance](#support-et-assistance)

---

## 🎯 Première connexion

### 📧 Création de votre compte

**Actuellement :** Votre compte est créé par un administrateur
**Bientôt :** Inscription publique disponible

### 🔑 Première connexion

1. **Récupérer vos identifiants** depuis l'administrateur
2. **Se connecter** à l'API :
   ```
   POST /api/auth/token/
   {
     "email": "votre-email@fapag.com",
     "password": "votre-mot-de-passe"
   }
   ```
3. **Conserver votre token** pour les requêtes suivantes

---

## 💰 Utilisation quotidienne

### 📖 Consulter les cagnottes

```bash
# Voir toutes les cagnottes disponibles
GET /api/cagnottes/

# Voir une cagnotte spécifique
GET /api/cagnottes/{id}/

# Headers requis :
Authorization: Bearer votre-token-jwt
```

### 🎯 Participer à une cagnotte

```bash
# Créer une participation
POST /api/participations/
{
  "cagnotte": 1,
  "montant": 50.00,
  "message": "Je soutiens cette cause !"
}

# Headers requis :
Authorization: Bearer votre-token-jwt
```

### 📊 Suivre vos participations

```bash
# Voir vos participations
GET /api/participations/

# Voir une participation spécifique
GET /api/participations/{id}/

# Headers requis :
Authorization: Bearer votre-token-jwt
```

---

## 🛡️ Sécurité de votre compte

### 🔐 Protection de votre mot de passe

**✅ À FAIRE :**
- Utiliser un mot de passe fort (12+ caractères)
- Changer votre mot de passe régulièrement
- Ne jamais partager vos identifiants

**❌ À NE JAMAIS FAIRE :**
- Utiliser le même mot de passe partout
- Écrire votre mot de passe sur papier
- Partager vos identifiants

### 📱 Sécurisation de votre appareil

- **Verrouiller** votre téléphone/ordinateur
- **Mettre à jour** régulièrement vos appareils
- **Utiliser un antivirus** à jour
- **Faire des sauvegardes** régulières

### 🚨 Signaux d'alerte

**Contactez immédiatement l'administrateur si :**
- Connexions depuis des lieux inconnus
- Modifications non autorisées de votre compte
- Messages d'erreur inhabituels

---

## 📞 Support et assistance

### 🆘 En cas de problème

1. **Vérifier** cette documentation
2. **Consulter** la section dépannage
3. **Contacter** l'administrateur système

### 📧 Contact administrateur

- **Email** : admin@fapag.com
- **Support** : support@fapag.com
- **Urgence** : +241 XX XX XX XX

---

## 🔧 Dépannage

### ❌ Problèmes de connexion

**Token expiré :**
```bash
# Renouveler votre token
POST /api/auth/token/refresh/
{
  "refresh": "votre-refresh-token"
}
```

**Mot de passe oublié :**
- Contacter l'administrateur système
- Procédure de réinitialisation sécurisée

### 📱 Problèmes d'API

**Erreur 401 (Non autorisé) :**
- Vérifier que votre token est valide
- Renouveler votre token si nécessaire

**Erreur 403 (Interdit) :**
- Vérifier vos permissions
- Contacter l'administrateur si nécessaire

**Erreur 429 (Trop de requêtes) :**
- Attendre quelques minutes
- Réduire la fréquence de vos requêtes

---

## 📚 Ressources utiles

### 🔗 Liens importants

- **API Documentation** : `/swagger/`
- **Guide de sécurité** : `BONNES_PRATIQUES_SECURITE.md`
- **Support technique** : support@fapag.com

### 📖 Exemples de code

**Python avec requests :**
```python
import requests

# Connexion
response = requests.post('http://votre-api.com/api/auth/token/', json={
    'email': 'votre-email@fapag.com',
    'password': 'votre-mot-de-passe'
})

token = response.json()['access']

# Requête authentifiée
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://votre-api.com/api/cagnottes/', headers=headers)
print(response.json())
```

**JavaScript avec fetch :**
```javascript
// Connexion
const response = await fetch('http://votre-api.com/api/auth/token/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        email: 'votre-email@fapag.com',
        password: 'votre-mot-de-passe'
    })
});

const {access} = await response.json();

// Requête authentifiée
const cagnottes = await fetch('http://votre-api.com/api/cagnottes/', {
    headers: {'Authorization': `Bearer ${access}`}
});
```

---

## ✅ Checklist utilisateur

- [ ] Compte créé et activé
- [ ] Première connexion réussie
- [ ] Token JWT obtenu et conservé
- [ ] Mot de passe fort configuré
- [ ] Appareil sécurisé
- [ ] Documentation consultée

---

**🛡️ Votre sécurité est importante pour nous !**

*Dernière mise à jour : Août 2025*
