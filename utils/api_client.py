"""
api_client.py

This module contains the APIClient class for interacting with the Books API. It provides methods for
sending GET, POST, DELETE, and PUT requests.

Classes:
    APIClient: A client for interacting with the Books API.

Functions:
    get: Sends a GET request to the API.
    post: Sends a POST request to the API.
    delete: Sends a DELETE request to the API.
    put: Sends a PUT request to the API.
"""

import requests
from utils.config import BASE_URL, TIMEOUT
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIClient:
    """
    A client for interacting with the Books API.

    Attributes:
        base_url (str): The base URL for the API.
        timeout (int): The timeout for API requests.
        session (requests.Session): The session object for making requests.
    """

    def __init__(self, base_url: str = BASE_URL, timeout: int = TIMEOUT):
        """
        Initializes the APIClient with the given base URL and timeout.

        Args:
            base_url (str): The base URL for the API. Defaults to BASE_URL.
            timeout (int): The timeout for API requests. Defaults to TIMEOUT.
        """
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, endpoint: str, params: dict = None, headers: dict = None) -> requests.Response:
        """
        Sends a GET request to the API.

        Args:
            endpoint (str): The API endpoint.
            params (dict, optional): The query parameters for the request. Defaults to None.
            headers (dict, optional): The headers for the request. Defaults to None.

        Returns:
            requests.Response: The response object from the API request.
        """
        url = f"{self.base_url}/{endpoint}"
        logger.info(f"GET {url}")
        response = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
        logger.info(f"Response: {response.status_code} {response.json()}")
        response.raise_for_status()
        return response

    def post(self, endpoint: str, data: dict = None, json: dict = None, headers: dict = None) -> requests.Response:
        """
        Sends a POST request to the API.

        Args:
            endpoint (str): The API endpoint.
            data (dict, optional): The form data for the request. Defaults to None.
            json (dict, optional): The JSON payload for the request. Defaults to None.
            headers (dict, optional): The headers for the request. Defaults to None.

        Returns:
            requests.Response: The response object from the API request.
        """
        url = f"{self.base_url}/{endpoint}"
        logger.info(f"POST {url}")
        response = self.session.post(url, data=data, json=json, headers=headers, timeout=self.timeout)
        logger.info(f"Response: {response.status_code} {response.json()}")
        response.raise_for_status()
        return response

    def delete(self, endpoint: str, params: dict = None, headers: dict = None) -> requests.Response:
        """
        Sends a DELETE request to the API.

        Args:
            endpoint (str): The API endpoint.
            params (dict, optional): The query parameters for the request. Defaults to None.
            headers (dict, optional): The headers for the request. Defaults to None.

        Returns:
            requests.Response: The response object from the API request.
        """
        url = f"{self.base_url}/{endpoint}"
        logger.info(f"DELETE {url}")
        response = self.session.delete(url, params=params, headers=headers, timeout=self.timeout)
        logger.info(f"Response: {response.status_code} {response.json()}")
        response.raise_for_status()
        return response

    def put(self, endpoint: str, params: dict = None, data: dict = None, json: dict = None, headers: dict = None) -> requests.Response:
        """
        Sends a PUT request to the API.

        Args:
            endpoint (str): The API endpoint.
            params (dict, optional): The query parameters for the request. Defaults to None.
            data (dict, optional): The form data for the request. Defaults to None.
            json (dict, optional): The JSON payload for the request. Defaults to None.
            headers (dict, optional): The headers for the request. Defaults to None.

        Returns:
            requests.Response: The response object from the API request.
        """
        url = f"{self.base_url}/{endpoint}"
        logger.info(f"PUT {url}")
        response = self.session.put(url, params=params, data=data, json=json, headers=headers, timeout=self.timeout)
        logger.info(f"Response: {response.status_code} {response.json()}")
        response.raise_for_status()
        return response
