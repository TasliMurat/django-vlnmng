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
    slug = AutoSlugField(populate_from='name', unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    class Meta:
        unique_together = ['name', 'provider']
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class IntegrationExecution(models.Model):
    """
    Her entegrasyon için çalıştırılan işlemlerin geçmişi.
    Kullanıcının history ekranında göreceği veriler burada.
    """
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE,
                                   related_name='execution')
    triggered_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Durum takibi
    STATUS_CHOICES = [
        ('pending', 'Bekliyor'),
        ('running', 'Çalışıyor'),
        ('completed', 'Tamamlandı'),
        ('partial', 'Kısmi Başarılı'), # Bazı adımlar hatalıysa
        ('failed', 'Başarısız'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    
    # Filtreleme kriterleri (kullanıcının ne seçtiği)
    filter_criteria = models.JSONField(default=dict)  # {date_from, date_to, severities}
    
    
    class Meta:
        db_table = 'integration_execution'
        ordering = ['-started_at']


class ExecutionStep(models.Model):

    execution = models.ForeignKey(IntegrationExecution, on_delete=models.CASCADE, related_name='steps')
    step_name = models.CharField(max_length=50, db_index=True)
    
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=IntegrationExecution.STATUS_CHOICES, default='pending')
    
    # Bu adıma özel çıktılar (Örn: Fetch adımında -> {"total_vulns": 150})
    result_data = models.JSONField(default=dict, blank=True)
    
    # Hata varsa buraya
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ['started_at']