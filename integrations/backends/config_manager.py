from ..models import Integration


class IntegrationConfigService:
    @staticmethod
    def create_integration(name, provider, config_data, is_Active):
        """
        Creates a new integration.
        """
        # In a real app, encrypt sensitive keys in config_data here before saving.
        integration = Integration(
            name=name,
            provider=provider,
            config=config_data,  # Saves the dict as JSON
            is_active=is_Active
        )
        integration.save()
            
        return integration

    @staticmethod
    def update_integration(integration, base_data, config_data):
        """
        Updates an existing integration.
        """
        # Update standard fields
        integration.name = base_data.get('name')
        integration.is_active = base_data.get('is_active')
        
        # Update the JSON config
        # Note: You might want to merge with existing config if you support partial updates,
        # but for a full form save, replacing it is usually correct.
        integration.config = config_data
        
        integration.save()

        # Update M2M relation
        if 'allowed_users' in base_data:
            integration.allowed_users.set(base_data['allowed_users'])
            
        return integration