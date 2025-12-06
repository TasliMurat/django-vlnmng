# integrations/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import IntegrationExecution
from .factories import BackendFactory
import traceback

@shared_task
def run_integration_execution_task(execution_id):
    """
    Orchestrates the vulnerability scan process in the background.
    """
    try:
        # 1. Retrieve the execution Record
        execution = IntegrationExecution.objects.get(id=execution_id)
        
        # 2. Update Status to RUNNING
        execution.status = 'running'
        execution.save()

        # 3. Initialize the Backend (Tenable, Invicti, etc.)
        # We use the integration object linked to the history
        integration = execution.integration
        backend = BackendFactory.get_adapter(integration.provider, integration.config)

        backend.run_pipeline(execution)
        
    except IntegrationExecution.DoesNotExist:
        return "execution record not found."
        
    except Exception as e:
        # 7. specific Error Handling
        if 'execution' in locals():
            execution.status = 'failed'
            execution.error_message = f"{str(e)}\n{traceback.format_exc()}"
            execution.completed_at = timezone.now()
            execution.save()
        
        # Re-raise to let Celery know it failed (for retries/monitoring)
        raise e