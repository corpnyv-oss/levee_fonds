# 👨‍💼 Guide Administrateur Système - API FAPAG

## 📋 Table des matières
1. [Vue d'ensemble](#vue-densemble)
2. [Installation et configuration](#installation-et-configuration)
3. [Gestion des utilisateurs](#gestion-des-utilisateurs)
4. [Monitoring et sécurité](#monitoring-et-sécurité)
5. [Maintenance et sauvegarde](#maintenance-et-sauvegarde)
6. [Procédures d'urgence](#procédures-durgence)

---

## 🎯 Vue d'ensemble

### 🔑 Rôles et responsabilités
- **Gestion des comptes** : Création, modification, suppression
- **Configuration de la sécurité** : 2FA, rate limiting, webhooks
- **Monitoring** : Logs, alertes, performances
- **Maintenance** : Mises à jour, sauvegardes, migrations

### 🛡️ Niveau d'accès
- **Accès complet** à toutes les fonctionnalités
- **2FA obligatoire** pour la sécurité
- **Audit complet** de toutes les actions

---

## ⚙️ Installation et configuration

### 🚀 Déploiement initial

```bash
# 1. Cloner le repository
git clone https://github.com/fapag/collecte-backend.git
cd collecte-backend

# 2. Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate   # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configuration des variables d'environnement
cp .env.example .env
# Éditer .env avec les vraies valeurs
```

### 🔐 Configuration de sécurité

```bash
# Générer des clés secrètes
python manage.py generate_secret_key
python manage.py generate_jwt_key

# Variables d'environnement critiques
export DJANGO_SECRET_KEY="clé-générée-sécurisée"
export JWT_SECRET_KEY="clé-jwt-sécurisée"
export WEBHOOK_SECRET_KEY="clé-webhook-sécurisée"
export DATABASE_URL="postgresql://user:pass@host:port/db"

# Configuration des IPs autorisées pour les webhooks
export WEBHOOK_ALLOWED_IPS="192.168.1.100,10.0.0.50"
```

---

## 👥 Gestion des utilisateurs

### 🔑 Création d'un super utilisateur

```bash
# Créer le premier administrateur
python manage.py createsuperuser

# Email: admin@fapag.com
# Mot de passe: [mot de passe fort]
# Rôle: admin
```

### 📊 Gestion des comptes via Django Admin

```python
# Accéder à l'interface d'administration
# URL: http://votre-domaine.com/admin/

# Actions disponibles :
# - Créer/modifier/supprimer des utilisateurs
# - Gérer les rôles (utilisateur/admin)
# - Voir l'historique des connexions
# - Gérer les tentatives de connexion échouées
```

### 🔐 Configuration 2FA pour les administrateurs

```bash
# 1. L'administrateur doit configurer sa 2FA
POST /2fa/setup/
{
    "email": "admin@fapag.com",
    "password": "mot-de-passe"
}

# 2. Scanner le QR code avec Google Authenticator
# 3. Confirmer avec le token TOTP
POST /2fa/verify-setup/
{
    "email": "admin@fapag.com",
    "password": "mot-de-passe",
    "token": "123456"
}
```

---

## 🚨 Monitoring et sécurité

### 📊 Tableau de bord de sécurité

```python
# Métriques à surveiller quotidiennement
SECURITY_METRICS = {
    'failed_logins': 'Nombre de tentatives échouées',
    'rate_limit_violations': 'Violations de rate limiting',
    '2fa_failures': 'Échecs d\'authentification 2FA',
    'suspicious_ips': 'IPs suspectes détectées',
    'webhook_attempts': 'Tentatives d\'accès aux webhooks',
    'admin_actions': 'Actions des administrateurs'
}
```

### 🔍 Vérification des logs

```bash
# Logs de sécurité
tail -f logs/security.log

# Logs d'authentification
tail -f logs/auth.log

# Logs des webhooks
tail -f logs/webhook.log

# Recherche d'activité suspecte
grep "FAILED" logs/auth.log
grep "suspicious" logs/security.log
```

### 🚦 Configuration des alertes

```python
# Alertes automatiques à configurer
ALERTS_CONFIG = {
    'failed_logins_threshold': 10,  # Alerte après 10 échecs
    'rate_limit_violations': True,  # Toutes les violations
    'admin_login_attempts': True,   # Toutes les tentatives admin
    'webhook_failures': True,       # Échecs de webhooks
    'database_errors': True,        # Erreurs de base de données
}
```

---

## 🔧 Maintenance et sauvegarde

### 📦 Mises à jour

```bash
# 1. Sauvegarde avant mise à jour
python manage.py dumpdata > backup_$(date +%Y%m%d).json

# 2. Mise à jour du code
git pull origin main

# 3. Mise à jour des dépendances
pip install -r requirements.txt

# 4. Migration de la base de données
python manage.py migrate

# 5. Vérification post-mise à jour
python manage.py check --deploy
python test_securite_complet.py
```

### 💾 Sauvegarde de la base de données

```bash
# Sauvegarde PostgreSQL
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Sauvegarde des fichiers média
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/

# Sauvegarde des logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz logs/

# Rotation des sauvegardes (garder 30 jours)
find . -name "backup_*.sql" -mtime +30 -delete
```

### 🔄 Maintenance préventive

```bash
# Nettoyage des logs anciens
find logs/ -name "*.log" -mtime +90 -delete

# Nettoyage des tentatives de connexion échouées
python manage.py axes_reset

# Vérification de l'intégrité de la base
python manage.py check --database default

# Optimisation de la base de données
python manage.py dbshell
VACUUM ANALYZE;
```

---

## 🚨 Procédures d'urgence

### 🔴 Incident de sécurité critique

```python
# 1. Isolation immédiate
def emergency_lockdown():
    # Désactiver tous les comptes suspects
    User.objects.filter(is_suspicious=True).update(is_active=False)
    
    # Bloquer les IPs suspectes
    add_to_blacklist(suspicious_ips)
    
    # Notifier l'équipe de sécurité
    notify_security_team("CRITICAL_SECURITY_INCIDENT")
    
    # Journalisation
    logger.critical("SYSTÈME EN LOCKDOWN D'URGENCE")

# 2. Évaluation de l'incident
def assess_incident():
    # Analyser les logs récents
    # Identifier la source de l'attaque
    # Évaluer l'étendue des dégâts
    # Déterminer les actions correctives
```

### 🟡 Récupération post-incident

```bash
# 1. Analyse forensique
python manage.py security_audit --detailed

# 2. Nettoyage des comptes compromis
python manage.py cleanup_compromised_accounts

# 3. Réinitialisation des mots de passe
python manage.py force_password_reset --all-users

# 4. Vérification de la sécurité
python test_securite_complet.py
python test_penetration_basique.py

# 5. Documentation de l'incident
echo "Incident: $(date)" >> incidents.log
echo "Actions prises: ..." >> incidents.log
```

---

## 📊 Rapports et audit

### 📈 Rapports quotidiens

```python
# Génération automatique des rapports
def daily_security_report():
    report = {
        'date': timezone.now().date(),
        'total_logins': LoginAttempt.objects.filter(
            created_at__date=timezone.now().date()
        ).count(),
        'failed_logins': LoginAttempt.objects.filter(
            created_at__date=timezone.now().date(),
            success=False
        ).count(),
        '2fa_usage': TOTPDevice.objects.filter(
            last_used__date=timezone.now().date()
        ).count(),
        'suspicious_activities': SecurityEvent.objects.filter(
            created_at__date=timezone.now().date(),
            severity__in=['HIGH', 'CRITICAL']
        ).count()
    }
    
    # Envoyer le rapport par email
    send_security_report(report)
    return report
```

### 🔍 Audit de conformité

```bash
# Vérification de la conformité
python manage.py security_compliance_check

# Points de contrôle :
# - Variables d'environnement sécurisées
# - Clés secrètes changées
# - 2FA activée pour les admins
# - Rate limiting configuré
# - Logs de sécurité actifs
# - Sauvegardes récentes
```

---

## ✅ Checklist administrateur

### 🔒 Configuration de base
- [ ] Variables d'environnement sécurisées
- [ ] Clés secrètes générées et changées
- [ ] Base de données configurée et sécurisée
- [ ] 2FA configurée pour tous les administrateurs

### 🚦 Sécurité active
- [ ] Rate limiting configuré et testé
- [ ] Webhooks sécurisés avec HMAC
- [ ] Logs de sécurité activés et surveillés
- [ ] Alertes configurées et testées

### 📊 Monitoring
- [ ] Tableau de bord de sécurité configuré
- [ ] Rapports quotidiens automatisés
- [ ] Procédures d'incident documentées
- [ ] Tests de sécurité réguliers

### 🔄 Maintenance
- [ ] Sauvegardes automatisées et testées
- [ ] Procédure de mise à jour documentée
- [ ] Rotation des logs configurée
- [ ] Nettoyage préventif automatisé

---

## 📞 Contacts d'urgence

### 🆘 Équipe de sécurité
- **Responsable sécurité** : security@fapag.com
- **Hotline 24/7** : +241 XX XX XX XX
- **Escalade management** : management@fapag.com

### 🔧 Support technique
- **Administrateur système** : admin@fapag.com
- **Développeur principal** : dev@fapag.com
- **Architecte sécurité** : architect@fapag.com

---

**🛡️ La sécurité du système est entre vos mains !**

*Dernière mise à jour : Août 2025*
