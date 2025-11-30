from django.contrib import admin
from integrations.models import Integration, IntegrationType
# Register your models here.


class IntegrationAdmin(admin.ModelAdmin):
    list_display = ("name", "type",)
    prepopulated_fields = {"slug": ("type",)}


admin.site.register(Integration)
