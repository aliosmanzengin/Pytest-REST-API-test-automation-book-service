"""
utils/api_client.py

/v1/books/manipulation POST - Add book with no arguments but request payload as json contains fields (type, title, creation date)
/v1/books/manipulation DELETE - Delete book with arguments (id)
/v1/books/manipulation PUT - Change the name of the book with arguments (id) (NOTE: updated time should be changed as well)
/v1/books/manipulation GET - Returns “No implementation for GET method”
/v1/books/latest GET - Get all the latest added books limited by some amount with arguments (limit)
/v1/books/info GET - Get info(type, name etc …) about a book with arguments (ID)
/v1/books/ids GET - Get all ID of books by type with arguments (book_type)
example: http://127.0.0.1:5000/v1/books/ids?book_type=Satire
[
    {
        "type": "Satire",
        "title": "Book2",
        "id": "431d9caa-1cef-4408-a5a8-835d447b63f5",
        "creation_date": "2021-01-02",
        "updated_date_time": "2024-07-09T09:58:46.374373"
    }
]

Examples of requests:

$ curl http://127.0.0.1:5000/v1/books/latest?limit=1

$ curl http://127.0.0.1:5000/v1/books/info?id=1cabb8d8-cea1-47eb-9282-f688886f9011

$ curl -d '{"title":"Book1", "type":"Satire", "creation_date":"2021-01-02"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/v1/books/manipulation -vvv

"""
import requests
from utils.config import BASE_URL, TIMEOUT
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url: str = BASE_URL, timeout: int = TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, endpoint: str, params: dict = None, headers: dict = None) -> requests.Response:
        url = f"{self.base_url}/{endpoint}"
        logger.info(f"GET {url}")
        response = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
        logger.info(f"Response: {response.status_code} {response.json()}")
        response.raise_for_status()
        return response

    def post(self, endpoint: str, data: dict = None, json: dict = None, headers: dict = None) -> requests.Response:
        url = f"{self.base_url}/{endpoint}"
        logger.info(f"POST {url}")
        response = self.session.post(url, data=data, json=json, headers=headers, timeout=self.timeout)
        logger.info(f"Response: {response.status_code} {response.json()}")
        response.raise_for_status()
        return response

    def delete(self, endpoint: str, params: dict = None, headers: dict = None) -> requests.Response:
        url = f"{self.base_url}/{endpoint}"
        logger.info(f"DELETE {url}")
        response = self.session.delete(url, params=params, headers=headers, timeout=self.timeout)
        logger.info(f"Response: {response.status_code} {response.json()}")
        response.raise_for_status()
        return response

    def put(self, endpoint: str, params: dict = None, data: dict = None, json: dict = None, headers: dict = None) -> requests.Response:
        url = f"{self.base_url}/{endpoint}"
        logger.info(f"PUT {url}")
        response = self.session.put(url, params=params, data=data, json=json, headers=headers, timeout=self.timeout)
        logger.info(f"Response: {response.status_code} {response.json()}")
        response.raise_for_status()
        return response
