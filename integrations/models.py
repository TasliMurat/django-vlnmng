from django.db import models
# Create your models here.
from abc import ABC, abstractmethod
from autoslug import AutoSlugField

class IntegrationType(models.TextChoices):
    TENABLE_SC = 'tenable_sc', 'Tenable.SC'
    INVICTI = 'invicti', 'Invicti'



class SeverityLevel(models.TextChoices):
    IMPORTANT = 'important', 'Important'
    CRITICAL = 'critical', 'Critical'
    HIGH = 'high', 'High'
    MEDIUM = 'medium', 'Medium'
    LOW = 'low', 'Low'
    INFO = 'info', 'Info'

    

class Integration(models.Model):
    """Entegrasyon tanımları"""
    name = models.CharField(max_length=100)
    provider = models.CharField(max_length=20, choices=IntegrationType.choices)
    config = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    slug = AutoSlugField(populate_from='provider', unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    class Meta:
        unique_together = ['name', 'provider']
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class IntegrationHistory(models.Model):
    """
    Her entegrasyon için çalıştırılan işlemlerin geçmişi.
    Kullanıcının history ekranında göreceği veriler burada.
    """
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE,
                                   related_name='history')
    
    # İşlem detayları
    operation_type = models.CharField(max_length=50)  # 'fetch_vulnerabilities', 'create_tickets'
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # İstatistikler
    total_vulnerabilities = models.IntegerField(default=0)
    critical_count = models.IntegerField(default=0)
    high_count = models.IntegerField(default=0)
    medium_count = models.IntegerField(default=0)
    low_count = models.IntegerField(default=0)
    
    tickets_created = models.IntegerField(default=0)
    tickets_failed = models.IntegerField(default=0)
    
    # Durum takibi
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    
    # Filtreleme kriterleri (kullanıcının ne seçtiği)
    filter_criteria = models.JSONField(default=dict)  # {date_from, date_to, severities}
    
    triggered_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'integration_history'
        ordering = ['-started_at']