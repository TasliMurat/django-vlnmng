from django.shortcuts import render
from django.contrib import messages
# Create your views here.

from django.shortcuts import render
from django.http import JsonResponse
from users.decorators import has_integration_permission
from .models import Integration, IntegrationType, SeverityLevel
from integrations.adapters.tenable import TenableAdapter
from django.http import HttpResponse

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

def CreateUpdateConfigView(request, adapter_type):
    if request.method == 'POST':
        # 1. Get Form Data
        name = request.POST.get('integration_name', '')
        integration_type = adapter_type
        config = request.POST.get('adapter_config', {})

        # 2. Validation
        if not all([name, integration_type, config]):
            # You must RETURN here to stop execution
            return JsonResponse({'status': 'error', 'message': 'All fields are required.'}, status=400)

        # 3. Connection Test
        try:
            adapter = TenableAdapter({"access_key": "dnfkldsnfds", "secret_key": "lkdsfsdpof"}) 
            is_connected = adapter.validate_connection()

            if is_connected:
                # Logic to save to DB would go here
                return JsonResponse({'status': 'success', 'message': 'Connection is successful.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Connection failed.'}, status=400)
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    else:
        # For GET requests
        return HttpResponse("Tenable config page")