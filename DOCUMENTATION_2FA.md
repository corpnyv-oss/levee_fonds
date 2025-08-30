# 🔐 Guide d'utilisation de la 2FA (Authentification à deux facteurs)

## 📋 Table des matières
1. [Qu'est-ce que la 2FA ?](#quest-ce-que-la-2fa)
2. [Configuration initiale](#configuration-initiale)
3. [Connexion avec 2FA](#connexion-avec-2fa)
4. [Codes de sauvegarde](#codes-de-sauvegarde)
5. [Récupération de compte](#récupération-de-compte)
6. [Sécurité et bonnes pratiques](#sécurité-et-bonnes-pratiques)
7. [Dépannage](#dépannage)

---

## 🎯 Qu'est-ce que la 2FA ?

L'**authentification à deux facteurs (2FA)** ajoute une couche de sécurité supplémentaire à votre compte. En plus de votre mot de passe, vous devez fournir un code temporaire généré par votre téléphone.

### 🔒 Pourquoi la 2FA est-elle importante ?
- **Protection contre le vol de mot de passe**
- **Sécurisation des comptes administrateur**
- **Conformité aux standards de sécurité**
- **Protection des données sensibles**

---

## ⚙️ Configuration initiale

### 📱 Étape 1 : Installer Google Authenticator

1. **Android** : [Google Play Store](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2)
2. **iPhone** : [App Store](https://apps.apple.com/app/google-authenticator/id388497605)
3. **Alternative** : Authy, Microsoft Authenticator

### 🔑 Étape 2 : Configurer la 2FA

1. **Se connecter** à votre compte administrateur
2. **Aller sur** `/2fa/setup/`
3. **Fournir** vos identifiants :
   ```json
   {
     "email": "votre-email@fapag.com",
     "password": "votre-mot-de-passe"
   }
   ```

### 📱 Étape 3 : Scanner le QR Code

1. **Ouvrir** Google Authenticator
2. **Appuyer** sur le bouton "+"
3. **Scanner** le QR code affiché
4. **Vérifier** que le compte apparaît

### ✅ Étape 4 : Confirmer la configuration

1. **Récupérer** le code à 6 chiffres dans Google Authenticator
2. **Envoyer** la confirmation :
   ```json
   {
     "email": "votre-email@fapag.com",
     "password": "votre-mot-de-passe",
     "token": "123456"
   }
   ```
3. **Sauvegarder** les codes de sauvegarde

---

## 🔐 Connexion avec 2FA

### 📝 Processus de connexion

1. **Saisir** votre email et mot de passe
2. **Récupérer** le code à 6 chiffres dans Google Authenticator
3. **Envoyer** la requête de connexion :
   ```json
   {
     "email": "votre-email@fapag.com",
     "password": "votre-mot-de-passe",
     "token": "123456"
   }
   ```

### ⚡ Codes temporaires

- **Durée de vie** : 30 secondes
- **Fenêtre de tolérance** : ±30 secondes
- **Génération automatique** : Toutes les 30 secondes

---

## 🆘 Codes de sauvegarde

### 📋 Qu'est-ce que c'est ?

Les **codes de sauvegarde** sont des codes à 8 chiffres qui permettent de récupérer l'accès à votre compte si vous perdez votre téléphone.

### 💾 Conservation sécurisée

**✅ À FAIRE :**
- Imprimer et stocker dans un coffre-fort
- Sauvegarder dans un gestionnaire de mots de passe
- Partager avec un contact de confiance

**❌ À NE PAS FAIRE :**
- Stocker sur votre ordinateur
- Envoyer par email
- Partager sur les réseaux sociaux

### 🔄 Utilisation des codes

1. **Se connecter** avec email et mot de passe
2. **Utiliser** un code de sauvegarde au lieu du token 2FA
3. **Le code devient invalide** après utilisation

---

## 🔄 Récupération de compte

### 📱 Perte de téléphone

1. **Utiliser** un code de sauvegarde
2. **Configurer** la 2FA sur un nouveau téléphone
3. **Régénérer** de nouveaux codes de sauvegarde

### 🔑 Mot de passe oublié

1. **Contacter** l'administrateur système
2. **Procédure** de réinitialisation sécurisée
3. **Reconfiguration** de la 2FA obligatoire

---

## 🛡️ Sécurité et bonnes pratiques

### 🔒 Sécurisation du téléphone

- **Verrouillage** par code PIN ou biométrie
- **Mise à jour** régulière du système
- **Antivirus** à jour
- **Sauvegarde** régulière

### 📱 Gestion des applications

- **Google Authenticator** : Application officielle
- **Vérification** de la source des applications
- **Désinstallation** des versions non officielles

### 🚨 Signaux d'alerte

**Contactez immédiatement l'administrateur si :**
- Codes 2FA rejetés sans raison
- Connexions depuis des lieux inconnus
- Modifications non autorisées de votre compte

---

## 🔧 Dépannage

### ❌ Code 2FA rejeté

**Causes possibles :**
1. **Désynchronisation horaire** : Vérifiez l'heure de votre téléphone
2. **Code expiré** : Attendez le prochain code (30 secondes)
3. **Application incorrecte** : Vérifiez que vous utilisez Google Authenticator

**Solutions :**
1. **Synchroniser** l'heure de votre téléphone
2. **Attendre** le prochain code
3. **Vérifier** la configuration de l'application

### 📱 Problèmes avec Google Authenticator

**Réinstallation :**
1. **Désinstaller** l'application
2. **Réinstaller** depuis la boutique officielle
3. **Reconfigurer** la 2FA avec un nouveau QR code

### 🔑 Codes de sauvegarde perdus

**Solution :**
1. **Contacter** l'administrateur système
2. **Procédure** de réinitialisation sécurisée
3. **Reconfiguration** complète de la 2FA

---

## 📞 Support et assistance

### 🆘 En cas de problème

1. **Vérifier** cette documentation
2. **Consulter** la section dépannage
3. **Contacter** l'administrateur système

### 📧 Contact administrateur

- **Email** : admin@fapag.com
- **Urgence** : +241 XX XX XX XX
- **Horaires** : Lundi-Vendredi, 8h-18h

---

## 📚 Ressources supplémentaires

### 🔗 Liens utiles

- [Guide Google Authenticator](https://support.google.com/accounts/answer/1066447)
- [Bonnes pratiques 2FA](https://www.ncsc.gov.uk/collection/device-security-guidance)
- [Sécurité des mots de passe](https://haveibeenpwned.com/)

### 📖 Documentation technique

- [API 2FA](../collecte/views_2fa.py)
- [Modèles 2FA](../collecte/models_2fa.py)
- [Tests de sécurité](../test_securite_complet.py)

---

## ✅ Checklist de sécurité

- [ ] 2FA configurée sur votre compte
- [ ] Codes de sauvegarde sauvegardés de manière sécurisée
- [ ] Téléphone verrouillé par code PIN ou biométrie
- [ ] Google Authenticator installé et configuré
- [ ] Heure du téléphone synchronisée
- [ ] Codes de sauvegarde testés

---

**🛡️ La sécurité de votre compte est entre vos mains !**

*Dernière mise à jour : Août 2025*
