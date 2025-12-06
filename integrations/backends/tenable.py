from typing import List, Dict, Any
from datetime import datetime
from .base import BaseBackend
import logging
from integrations.models import Integration, IntegrationExecution, ExecutionStep
import requests
from django.utils import timezone

class TenableSteps:
    FETCH = 'tenable_fetch'
    NORMALIZE = 'tenable_normalize'
    ASSET_MAP = 'asset_mapping'
    JIRA = 'jira_sync'


class TenableBackend(BaseBackend):
    def __init__(self, config):
        base_url = config.get("base_url")
        access_key = config.get("access_key")
        secret_key = config.get("secret_key")

    def fetch_vulnerabilities(self, date_from, date_to, severities):
        pass

    def normalize_vulnerability(self, raw_data):
        pass

    def run_pipeline(self, execution):
        try:
            step_fetch = self._create_step(execution, TenableSteps.FETCH)
            print("zafiyetler çekiliyor.")
            self._complete_step(step_fetch, {"feth": "tamamlandı"})

            step_normalize = self._create_step(execution, TenableSteps.NORMALIZE)
            print("normalize ediliyor.")
            self._complete_step(step_normalize, {"feth": "tamamlandı"})

            execution.status = 'completed'
            execution.completed_at = timezone.now()
            execution.save()
        
        except Exception as e:
            execution.status = 'failed'
            execution.save()
            raise e
    
    def _create_step(self, integration_execution, step):
        execution_step = ExecutionStep(
            execution = integration_execution,
            step_name = step,
            started_at = timezone.now(),
            status = "running"
        )
        return execution_step

    def _complete_step(self,step: ExecutionStep, result_data) -> None:
        step.status = "completed"
        step.completed_at = timezone.now()
        step.result_data = result_data
        step.save()

    def _test_connection(self):
        try:
            # 1. Initialize the client
            # We assume verify=False for internal SCs often using self-signed certs.
            # If you have valid certs, change this to True.
            response = requests.get("https://692322da09df4a4923246cd0.mockapi.io/tenable_sc/testconnection")
            return response

        except Exception as e:
            return f"Unexpected Error: {str(e)}"