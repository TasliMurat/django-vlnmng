from django.db import models
from django.contrib.auth.models import AbstractUser
from integrations.models import Integration

# Create your models here.


class User(AbstractUser):
    """Genişletilmiş kullanıcı modeli
    username, firstname, lastname, is_staff, is_active"""
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100, blank=True)
    is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class UserIntegrationPermission(models.Model):
    """Kullanıcıların hangi entegrasyonlara erişebileceğini tanımlar"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='integration_permissions')
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE)
    can_read = models.BooleanField(default=True)
    can_execute = models.BooleanField(default=False)
    can_config = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    granted_at = models.DateTimeField(auto_now_add=True)
    granted_by = models.ForeignKey(User, on_delete=models.SET_NULL, 
                                  null=True, related_name='granted_permissions')
    
    class Meta:
        unique_together = ['user', 'integration']
    
    def __str__(self):
        return f"{self.user.username} -> {self.integration.name}"
