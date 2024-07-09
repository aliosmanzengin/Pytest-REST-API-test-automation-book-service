"""
conftest.py

This module contains the pytest configuration and fixtures for setting up and tearing down the test environment
for the Books API tests.

Fixtures:
    api_client: Provides an instance of the APIClient for making API requests.
    teardown: Automatically removes all books after the test session ends.
"""

import csv
import pytest
from tests.helpers import delete_book, add_book, remove_all_books
from utils.api_client import APIClient


@pytest.fixture(scope='session')
def api_client():
    """
    Fixture to provide an instance of the APIClient for the test session.

    Returns:
        APIClient: An instance of the APIClient to interact with the Books API.
    """
    return APIClient()


@pytest.fixture(scope='session', autouse=True)
def teardown(api_client):
    """
    Fixture to perform teardown operations after the test session ends.
    This fixture is automatically executed and removes all books using the APIClient.

    Args:
        api_client (APIClient): An instance of the APIClient to interact with the Books API.
    """
    yield
    remove_all_books(api_client)
