

from .backends.tenable import TenableBackend
# from .adapters.invicti import InvictiAdapter

class BackendFactory:
    @staticmethod
    def get_adapter(provider, config):
        """
        Integration modelindeki 'type' alanına göre doğru adapter'ı döndürür.
        """
        if provider == 'tenable_sc':
            return TenableBackend(config)
        # elif integration_instance.type == 'invicti':
        #     return InvictiAdapter(integration_instance.config)
        else:
            raise ValueError("Bilinmeyen entegrasyon türü!")