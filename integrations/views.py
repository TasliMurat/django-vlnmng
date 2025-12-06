from django.shortcuts import get_object_or_404, render
from django.contrib import messages

from integrations.tasks import run_integration_execution_task
# Create your views here.
from .backends.config_manager import IntegrationConfigService
from integrations.factories import BackendFactory
from users.decorators import has_integration_permission
from .models import Integration, IntegrationExecution, SeverityLevel
from django.http import HttpResponse, JsonResponse
import json
from .forms import IntegrationConfigForm, IntegrationRunForm
import traceback


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
    

# @login_required
# @require_POST
def run_integration(request, slug):
    """
    Herhangi bir entegrasyonu (Tenable, Invicti, Nessus vs.) çalıştıran 
    tek ve merkezi fonksiyon.
    """
    # 1. Entegrasyonu ID'sine göre bul
    integration = get_object_or_404(Integration, slug=slug)

    if not integration.is_active:
        return JsonResponse({"status": "error", "message": "Bu entegrasyon pasif durumda."}, status=400)

    form = IntegrationRunForm(request.POST)
    if form.is_valid():
        filters = form.cleaned_data
        json_filters = {
            "date_from": filters['date_from'].isoformat() if filters['date_from'] else None,
            "date_to": filters['date_to'].isoformat() if filters['date_to'] else None,
            "severities": filters['severities']
        }

        # 4. History Kaydı Oluştur (PENDING)
        execution = IntegrationExecution.objects.create(
            integration=integration,
            triggered_by=request.user,
            filter_criteria=filters,
            status="pending"
        )

        # 5. Generic Celery Task'ini Tetikle
        # Sadece history ID'sini gönderiyoruz. Task gerisini halledecek.
        task = run_integration_execution_task.delay(execution.id)

        return JsonResponse({
            "status": "success", 
            "message": f"{integration.name} taraması başlatıldı.",
            "execution_id": execution.id,
            "task_id": task.id
        })

    else:
        # Form geçersizse hataları dön
        return JsonResponse({
            "status": "error",
            "message": "Filtre parametreleri hatalı.",
            "errors": form.errors
        }, status=400)