# users/decorators.py
from functools import wraps
from django.http import HttpResponseForbidden
from .models import UserIntegrationPermission, Integration

def has_integration_permission(integration_type, permission="can_execute"):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return HttpResponseForbidden("Authentication required")

            try:
                integration = Integration.objects.get(type=integration_type)
                perm = UserIntegrationPermission.objects.get(user=user, integration=integration)
            except (Integration.DoesNotExist, UserIntegrationPermission.DoesNotExist):
                return HttpResponseForbidden("No permission for this integration")

            if not getattr(perm, permission, False):
                return HttpResponseForbidden("Insufficient permission")

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
