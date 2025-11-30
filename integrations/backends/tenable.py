from typing import List, Dict, Any
from datetime import datetime
from .base import BaseBackend
import logging
from integrations.models import Integration
import requests

class TenableBackend(BaseBackend):
    def __init__(self, config):
        print(type(config))
        base_url = config.get("base_url")
        access_key = config.get("access_key")
        secret_key = config.get("secret_key")

    def fetch_vulnerabilities(self, date_from, date_to, severities):
        pass

    def normalize_vulnerability(self, raw_data):
        pass
    
    def _test_connection(self):
        try:
            # 1. Initialize the client
            # We assume verify=False for internal SCs often using self-signed certs.
            # If you have valid certs, change this to True.
            response = requests.get("https://692322da09df4a4923246cd0.mockapi.io/tenable_sc/testconnection")
            return response.status_code

        except Exception as e:
            return f"Unexpected Error: {str(e)}"