from django.shortcuts import get_object_or_404, render
from django.contrib import messages
# Create your views here.
from .backends.config_manager import IntegrationConfigService
from integrations.factories import BackendFactory
from users.decorators import has_integration_permission
from .models import Integration, SeverityLevel
from django.http import HttpResponse, JsonResponse
import json
from .forms import IntegrationConfigForm
import traceback

@has_integration_permission("tenable_sc", "can_execute")
def run_tenable(request):
    # Burada şimdilik dummy response
    return JsonResponse({"status": "Tenable çalıştı"})

@has_integration_permission("invicti", "can_execute")
def run_invicti(request):
    return JsonResponse({"status": "Invicti çalıştı"})

def integration_detail(request, pk):
    integration = Integration.objects.get(pk=pk)
    severities = SeverityLevel.choices
    return render(request, "integrations/detail.html", {"integration": integration, "severities": severities})

def IntegrationConfigView(request, provider, pk=None):
    if request.method == 'POST':
        form = IntegrationConfigForm(request.POST)

        if form.is_valid():
            # Verileri cleaned_data üzerinden alıyoruz
            name = form.cleaned_data["name"]
            config = form.cleaned_data["config"]
            is_active = form.cleaned_data["is_active"] # required=False olsa bile buraya True/False gelir.

            try:
                # Backend Factory çağır
                adapter = BackendFactory.get_adapter(provider, config=config) 
                is_connected = adapter.validate_connection()

                if is_connected:
                    if pk:
                         IntegrationConfigService.update_integration(
                             name=name, provider=provider, config=config, is_active=is_active, pk=pk
                         )
                    else:
                         IntegrationConfigService.create_integration(
                             name=name, provider=provider, config=config, is_active=is_active
                         )

                    return JsonResponse({'status': 'success', 'message': 'Connection is successful.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Connection failed.'}, status=400)
            
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': str(e),
                    'traceback': traceback.format_exc()
                }, status=500)
        
        else:
            # Form validasyon hataları
            return JsonResponse({
                'status': 'error',
                'message': 'Validasyon hatası',
                'errors': form.errors
            }, status=400)

    else:
        return HttpResponse("Tenable config page")