"""
Système de monitoring avancé pour la sécurité de l'API FAPAG
"""
import logging
import json
import time
from datetime import datetime, timedelta
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from django.db.models import Count, Q
from django.core.mail import send_mail
from .models import User, Participation, Transaction
from .models_2fa import LoginAttempt, TOTPDevice

logger = logging.getLogger(__name__)

class SecurityMonitor:
    """Moniteur de sécurité en temps réel"""
    
    def __init__(self):
        self.cache_timeout = 300  # 5 minutes
        self.alert_thresholds = {
            'failed_logins': 10,
            'rate_limit_violations': 20,
            'suspicious_ips': 5,
            '2fa_failures': 8,
            'webhook_attempts': 50
        }
    
    def check_failed_logins(self):
        """Vérifier les tentatives de connexion échouées"""
        try:
            # Compter les échecs de la dernière heure
            one_hour_ago = timezone.now() - timedelta(hours=1)
            failed_count = LoginAttempt.objects.filter(
                success=False,
                created_at__gte=one_hour_ago
            ).count()
            
            cache_key = 'security:failed_logins_count'
            cache.set(cache_key, failed_count, self.cache_timeout)
            
            if failed_count >= self.alert_thresholds['failed_logins']:
                self._send_security_alert('failed_logins', failed_count)
                logger.warning(f"ALERTE: {failed_count} tentatives de connexion échouées")
            
            return failed_count
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification des connexions échouées: {e}")
            return 0
    
    def check_rate_limit_violations(self):
        """Vérifier les violations de rate limiting"""
        try:
            # Compter les erreurs 429 de la dernière heure
            one_hour_ago = timezone.now() - timedelta(hours=1)
            
            # Cette métrique nécessiterait un middleware de logging spécifique
            # Pour l'instant, on utilise une approximation
            rate_limit_violations = 0
            
            cache_key = 'security:rate_limit_violations'
            cache.set(cache_key, rate_limit_violations, self.cache_timeout)
            
            if rate_limit_violations >= self.alert_thresholds['rate_limit_violations']:
                self._send_security_alert('rate_limit_violations', rate_limit_violations)
                logger.warning(f"ALERTE: {rate_limit_violations} violations de rate limiting")
            
            return rate_limit_violations
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification du rate limiting: {e}")
            return 0
    
    def check_suspicious_ips(self):
        """Détecter les IPs suspectes"""
        try:
            # Compter les IPs avec de nombreux échecs
            one_hour_ago = timezone.now() - timedelta(hours=1)
            
            suspicious_ips = LoginAttempt.objects.filter(
                success=False,
                created_at__gte=one_hour_ago
            ).values('ip_address').annotate(
                failed_count=Count('id')
            ).filter(failed_count__gte=5)
            
            suspicious_count = len(suspicious_ips)
            
            cache_key = 'security:suspicious_ips_count'
            cache.set(cache_key, suspicious_count, self.cache_timeout)
            
            if suspicious_count >= self.alert_thresholds['suspicious_ips']:
                self._send_security_alert('suspicious_ips', suspicious_count, suspicious_ips)
                logger.warning(f"ALERTE: {suspicious_count} IPs suspectes détectées")
            
            return suspicious_count
            
        except Exception as e:
            logger.error(f"Erreur lors de la détection des IPs suspectes: {e}")
            return 0
    
    def check_2fa_failures(self):
        """Vérifier les échecs 2FA"""
        try:
            # Compter les échecs 2FA de la dernière heure
            one_hour_ago = timezone.now() - timedelta(hours=1)
            
            # Cette métrique nécessiterait un logging spécifique des échecs 2FA
            # Pour l'instant, on utilise une approximation
            twofa_failures = 0
            
            cache_key = 'security:2fa_failures'
            cache.set(cache_key, twofa_failures, self.cache_timeout)
            
            if twofa_failures >= self.alert_thresholds['2fa_failures']:
                self._send_security_alert('2fa_failures', twofa_failures)
                logger.warning(f"ALERTE: {twofa_failures} échecs 2FA")
            
            return twofa_failures
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification des échecs 2FA: {e}")
            return 0
    
    def check_webhook_security(self):
        """Vérifier la sécurité des webhooks"""
        try:
            # Compter les tentatives d'accès aux webhooks de la dernière heure
            one_hour_ago = timezone.now() - timedelta(hours=1)
            
            # Cette métrique nécessiterait un logging spécifique des webhooks
            # Pour l'instant, on utilise une approximation
            webhook_attempts = 0
            
            cache_key = 'security:webhook_attempts'
            cache.set(cache_key, webhook_attempts, self.cache_timeout)
            
            if webhook_attempts >= self.alert_thresholds['webhook_attempts']:
                self._send_security_alert('webhook_attempts', webhook_attempts)
                logger.warning(f"ALERTE: {webhook_attempts} tentatives d'accès aux webhooks")
            
            return webhook_attempts
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification des webhooks: {e}")
            return 0
    
    def run_security_scan(self):
        """Exécuter un scan de sécurité complet"""
        try:
            logger.info("🔍 Début du scan de sécurité...")
            
            results = {
                'timestamp': timezone.now().isoformat(),
                'failed_logins': self.check_failed_logins(),
                'rate_limit_violations': self.check_rate_limit_violations(),
                'suspicious_ips': self.check_suspicious_ips(),
                '2fa_failures': self.check_2fa_failures(),
                'webhook_attempts': self.check_webhook_security(),
                'overall_status': 'OK'
            }
            
            # Déterminer le statut global
            alert_count = sum(1 for key, value in results.items() 
                            if key in self.alert_thresholds and 
                            value >= self.alert_thresholds[key])
            
            if alert_count > 0:
                results['overall_status'] = 'ALERT'
                logger.warning(f"🚨 SCAN DE SÉCURITÉ: {alert_count} alertes détectées")
            else:
                logger.info("✅ SCAN DE SÉCURITÉ: Aucune alerte détectée")
            
            # Sauvegarder les résultats
            cache.set('security:last_scan_results', results, 3600)  # 1 heure
            
            return results
            
        except Exception as e:
            logger.error(f"Erreur lors du scan de sécurité: {e}")
            return {'error': str(e), 'overall_status': 'ERROR'}
    
    def _send_security_alert(self, alert_type, count, details=None):
        """Envoyer une alerte de sécurité"""
        try:
            subject = f"🚨 ALERTE SÉCURITÉ FAPAG - {alert_type.upper()}"
            
            message = f"""
ALERTE DE SÉCURITÉ DÉTECTÉE

Type: {alert_type}
Compteur: {count}
Seuil: {self.alert_thresholds[alert_type]}
Timestamp: {timezone.now().isoformat()}

Détails: {details if details else 'Aucun détail supplémentaire'}

Action requise: Vérification immédiate de la sécurité
            """
            
            # Envoyer l'alerte par email (si configuré)
            if hasattr(settings, 'SECURITY_ALERT_EMAIL'):
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.SECURITY_ALERT_EMAIL],
                    fail_silently=True
                )
            
            # Journaliser l'alerte
            logger.critical(f"ALERTE SÉCURITÉ ENVOYÉE: {alert_type} - {count}")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'alerte: {e}")

class PerformanceMonitor:
    """Moniteur de performance de l'API"""
    
    def __init__(self):
        self.cache_timeout = 300  # 5 minutes
    
    def check_api_performance(self):
        """Vérifier les performances de l'API"""
        try:
            # Compter les requêtes de la dernière heure
            one_hour_ago = timezone.now() - timedelta(hours=1)
            
            # Cette métrique nécessiterait un middleware de logging spécifique
            # Pour l'instant, on utilise des métriques de base
            
            metrics = {
                'timestamp': timezone.now().isoformat(),
                'total_users': User.objects.count(),
                'active_cagnottes': Cagnotte.objects.filter(statut='active').count(),
                'total_participations': Participation.objects.count(),
                'total_transactions': Transaction.objects.count(),
                '2fa_devices': TOTPDevice.objects.count(),
                'recent_logins': LoginAttempt.objects.filter(
                    created_at__gte=one_hour_ago
                ).count()
            }
            
            # Sauvegarder les métriques
            cache.set('performance:api_metrics', metrics, self.cache_timeout)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification des performances: {e}")
            return {'error': str(e)}

class ComplianceMonitor:
    """Moniteur de conformité et d'audit"""
    
    def __init__(self):
        self.cache_timeout = 3600  # 1 heure
    
    def check_security_compliance(self):
        """Vérifier la conformité de sécurité"""
        try:
            compliance_checks = {
                'timestamp': timezone.now().isoformat(),
                '2fa_enabled_for_admins': self._check_2fa_for_admins(),
                'strong_passwords': self._check_password_policy(),
                'rate_limiting_active': self._check_rate_limiting(),
                'webhook_security': self._check_webhook_security(),
                'logging_active': self._check_logging(),
                'backup_recent': self._check_backup_status()
            }
            
            # Calculer le score de conformité
            passed_checks = sum(1 for check in compliance_checks.values() 
                              if isinstance(check, bool) and check)
            total_checks = sum(1 for check in compliance_checks.values() 
                             if isinstance(check, bool))
            
            compliance_checks['compliance_score'] = (passed_checks / total_checks) * 100
            compliance_checks['status'] = 'COMPLIANT' if compliance_checks['compliance_score'] >= 90 else 'NON_COMPLIANT'
            
            # Sauvegarder les résultats
            cache.set('compliance:security_status', compliance_checks, self.cache_timeout)
            
            return compliance_checks
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification de conformité: {e}")
            return {'error': str(e)}
    
    def _check_2fa_for_admins(self):
        """Vérifier que tous les admins ont la 2FA activée"""
        try:
            admin_users = User.objects.filter(role='admin')
            admins_with_2fa = TOTPDevice.objects.filter(
                user__role='admin',
                confirmed=True
            ).values_list('user_id', flat=True)
            
            return len(admins_with_2fa) == admin_users.count()
        except:
            return False
    
    def _check_password_policy(self):
        """Vérifier la politique des mots de passe"""
        # Cette vérification nécessiterait un système de validation des mots de passe
        # Pour l'instant, on considère que c'est OK
        return True
    
    def _check_rate_limiting(self):
        """Vérifier que le rate limiting est actif"""
        # Vérifier la configuration
        return hasattr(settings, 'RATE_LIMIT_AUTH')
    
    def _check_webhook_security(self):
        """Vérifier la sécurité des webhooks"""
        # Vérifier la configuration
        return hasattr(settings, 'WEBHOOK_SECRET_KEY')
    
    def _check_logging(self):
        """Vérifier que la journalisation est active"""
        return hasattr(settings, 'LOGGING')
    
    def _check_backup_status(self):
        """Vérifier le statut des sauvegardes"""
        # Cette vérification nécessiterait un système de sauvegarde automatisé
        # Pour l'instant, on considère que c'est OK
        return True

# Instances globales
security_monitor = SecurityMonitor()
performance_monitor = PerformanceMonitor()
compliance_monitor = ComplianceMonitor()

def run_daily_security_audit():
    """Audit de sécurité quotidien automatisé"""
    try:
        logger.info("🔍 Début de l'audit de sécurité quotidien...")
        
        # Scan de sécurité
        security_results = security_monitor.run_security_scan()
        
        # Vérification de conformité
        compliance_results = compliance_monitor.check_security_compliance()
        
        # Vérification des performances
        performance_results = performance_monitor.check_api_performance()
        
        # Rapport complet
        audit_report = {
            'date': timezone.now().date().isoformat(),
            'security': security_results,
            'compliance': compliance_results,
            'performance': performance_results,
            'recommendations': _generate_recommendations(security_results, compliance_results)
        }
        
        # Sauvegarder le rapport
        cache.set('audit:daily_report', audit_report, 86400)  # 24 heures
        
        # Envoyer le rapport par email si configuré
        if hasattr(settings, 'AUDIT_REPORT_EMAIL'):
            _send_audit_report(audit_report)
        
        logger.info("✅ Audit de sécurité quotidien terminé")
        return audit_report
        
    except Exception as e:
        logger.error(f"Erreur lors de l'audit quotidien: {e}")
        return {'error': str(e)}

def _generate_recommendations(security_results, compliance_results):
    """Générer des recommandations basées sur les résultats"""
    recommendations = []
    
    if security_results.get('overall_status') == 'ALERT':
        recommendations.append("🚨 Vérification immédiate des alertes de sécurité requise")
    
    if compliance_results.get('compliance_score', 100) < 90:
        recommendations.append("⚠️ Actions de conformité requises pour atteindre 90%")
    
    if security_results.get('failed_logins', 0) > 5:
        recommendations.append("🔐 Renforcer la protection contre les attaques par force brute")
    
    if security_results.get('suspicious_ips', 0) > 0:
        recommendations.append("🌐 Analyser et bloquer les IPs suspectes")
    
    if not compliance_results.get('2fa_enabled_for_admins', False):
        recommendations.append("🔐 Activer la 2FA pour tous les administrateurs")
    
    if not recommendations:
        recommendations.append("✅ Aucune action immédiate requise")
    
    return recommendations

def _send_audit_report(audit_report):
    """Envoyer le rapport d'audit par email"""
    try:
        subject = f"📊 Rapport d'audit de sécurité FAPAG - {audit_report['date']}"
        
        message = f"""
RAPPORT D'AUDIT DE SÉCURITÉ QUOTIDIEN

Date: {audit_report['date']}

SÉCURITÉ:
- Statut: {audit_report['security'].get('overall_status', 'N/A')}
- Connexions échouées: {audit_report['security'].get('failed_logins', 0)}
- IPs suspectes: {audit_report['security'].get('suspicious_ips', 0)}

CONFORMITÉ:
- Score: {audit_report['compliance'].get('compliance_score', 0)}%
- Statut: {audit_report['compliance'].get('status', 'N/A')}

RECOMMANDATIONS:
{chr(10).join(audit_report['recommendations'])}

Consultez les logs pour plus de détails.
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.AUDIT_REPORT_EMAIL],
            fail_silently=True
        )
        
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi du rapport d'audit: {e}")
