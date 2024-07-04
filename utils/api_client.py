# utils/api_client.py
import requests
from config import BASE_URL, TIMEOUT
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url=BASE_URL, timeout=TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, endpoint, params=None, headers=None):
        url = f"{self.base_url}/{endpoint}"
        logger.info(f"GET {url}")
        response = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        logger.info(f"Response: {response.status_code} {response.json()}")
        return response.json()

    def post(self, endpoint, data=None, json=None, headers=None):
        url = f"{self.base_url}/{endpoint}"
        logger.info(f"POST {url}")
        response = self.session.post(url, data=data, json=json, headers=headers, timeout=self.timeout)
        response.raise_
