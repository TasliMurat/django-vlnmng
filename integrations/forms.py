from django import forms
from .models import IntegrationType

class IntegrationConfigForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, error_messages={'required': 'Lütfen bir entegrasyon adı giriniz.'})
    config = forms.JSONField(required=True, error_messages={'required': 'Lütfen konfigürasyon bilgilerini giriniz.'})
    is_active = forms.BooleanField(required=False)