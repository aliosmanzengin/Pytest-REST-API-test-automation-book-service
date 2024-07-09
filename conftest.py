# conftest.py
import pytest

from tests.helpers import delete_book, add_book
from utils.api_client import APIClient


@pytest.fixture(scope='session')
def api_client():
    return APIClient()
