# apps/integrations/services/base.py

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BaseBackend(ABC):
    """
    Tüm entegrasyon servislerinin türetileceği temel sınıf.
    Her entegrasyon bu arayüzü implement etmek zorunda.
    """
    
    def __init__(self):
        """
        Her servis kendi integration config'i ile başlatılır.
        Config içinde API URL, key vs. bulunur.
        """
        
    @abstractmethod
    def fetch_vulnerabilities(self, 
                             date_from: datetime, 
                             date_to: datetime,
                             severities: List[str]) -> List[Dict[str, Any]]:
        """
        Belirtilen kriterlere göre zafiyetleri çeker.
        Her alt sınıf kendi API'sine göre bunu implement eder.
        
        Returns:
            Normalize edilmiş zafiyet listesi
        """
        pass
    
    @abstractmethod
    def normalize_vulnerability(self, raw_data: Dict) -> Dict[str, Any]:
        """
        API'den gelen ham veriyi standart formata dönüştürür.
        Bu sayede farklı kaynaklardan gelen veriler aynı yapıda olur.
        """
        pass
    
    def validate_connection(self) -> bool:
        """
        API bağlantısının çalışıp çalışmadığını test eder.
        Tüm servisler için ortak bir işlem.
        """
        try:
            response = self._test_connection()
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Connection validation failed: {str(e)}")
            return False
    
    @abstractmethod
    def _test_connection(self):
        """Her servis kendi test endpoint'ini çağırır"""
        pass