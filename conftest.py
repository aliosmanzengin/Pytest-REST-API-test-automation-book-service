"""
conftest.py

This module contains the pytest configuration and fixtures for setting up and tearing down the test environment
for the Books API tests.

Fixtures:
    api_client: Provides an instance of the APIClient for making API requests.
    teardown: Automatically removes all books after the test session ends.
"""

import csv
import os
import shutil

import pytest
from tests.helpers import delete_book, add_book, remove_all_books
from utils.api_client import APIClient, logger
from datetime import datetime


@pytest.fixture(scope='session', autouse=True)
def clean_reports():
    """
    Clean up the old reports before the test session starts.

    This fixture runs automatically before any tests are executed. It ensures that old Allure report
    directories are removed and a new reports directory is created.
    """

    allure_results_dir = "allure-results"
    if os.path.exists(allure_results_dir):
        shutil.rmtree(allure_results_dir)
    os.makedirs(allure_results_dir)

    report_dir = "reports"
    if os.path.exists(report_dir):
        shutil.rmtree(report_dir)
    os.makedirs(report_dir)


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


def pytest_sessionfinish(session, exitstatus):
    """
    Generate the Allure report at the end of the test session.

    This function is called after all tests have been executed. It generates the Allure report
    and saves it in a directory named with the current date. Optionally, it can serve the report
    automatically.

    Args:
        session: The pytest session object.
        exitstatus: The exit status of the pytest session.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d')
    report_dir = f"reports/allure_report_{timestamp}"
    logger.info(f"Generating Allure report on directory: {report_dir}")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    os.system(f"allure generate allure-results --clean -o {report_dir}")
    # Uncomment the next line if you want to open the report automatically
    os.system(f"allure open {report_dir}")

