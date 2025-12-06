from django import forms
from .models import IntegrationType
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import SeverityLevel  # Modelinizdeki severity seçeneklerini kullanın

class IntegrationConfigForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, error_messages={'required': 'Lütfen bir entegrasyon adı giriniz.'})
    config = forms.JSONField(required=True, error_messages={'required': 'Lütfen konfigürasyon bilgilerini giriniz.'})
    is_active = forms.BooleanField(required=False)


class IntegrationRunForm(forms.Form):
    date_from = forms.DateField(
        label="Başlangıç Tarihi",
        required=True,
    )
    date_to = forms.DateField(
        label="Bitiş Tarihi",
        required=False,
    )
    severities = forms.MultipleChoiceField(
        label="Risk Seviyeleri",
        choices=SeverityLevel.choices,
        required=False,
    )

    def clean(self):
        """
        Tarih mantığını kontrol ettiğimiz yer.
        """
        cleaned_data = super().clean()
        date_from = cleaned_data.get("date_from")
        date_to = cleaned_data.get("date_to")

        if date_from and date_to:
            if date_from > date_to:
                raise ValidationError("Başlangıç tarihi bitiş tarihinden büyük olamaz.")
                # Bu hata form.errors içinde 'non_field_errors' olarak döner.
        
        return cleaned_data