# conftest.py
import csv

import pytest

from tests.helpers import delete_book, add_book, remove_all_books
from utils.api_client import APIClient


@pytest.fixture(scope='session')
def api_client():
    return APIClient()


@pytest.fixture(scope='session', autouse=True)
def teardown(api_client):
    yield
    remove_all_books(api_client)
