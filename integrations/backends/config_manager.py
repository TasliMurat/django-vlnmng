from django.shortcuts import get_object_or_404
from ..models import Integration


class IntegrationConfigService:
    @staticmethod
    def create_integration(name, provider, config, is_active):
        """
        Creates a new integration.
        """
        # In a real app, encrypt sensitive keys in config_data here before saving.

        integration = Integration(
            name=name,
            provider=provider,
            config=config,  # Saves the dict as JSON
            is_active=is_active
        )
        integration.save()
            
        return integration

    @staticmethod
    def update_integration(name, provider, config, is_active, pk):
        """
        Updates an existing integration.
        """
        integration = get_object_or_404(Integration, pk=pk, provider=provider)
        integration.name = name
        integration.provider = provider
        integration.config = config
        integration.is_active = is_active
        integration.save()
    
        
        integration.save()

            
        return integration