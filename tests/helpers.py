"""
helpers.py

This module contains helper functions for interacting with the Books API.

Functions:
    add_book: Adds a new book to the API.
    delete_book: Deletes a book from the API by ID.
    update_book: Updates the title of a book in the API by ID.
    get_latest_books: Retrieves the latest books from the API.
    get_books_by_type: Retrieves books by type from the API.
    get_book_info: Retrieves information about a specific book by ID from the API.
    get_all_books: Retrieves all books from the API.
    remove_all_books: Removes all books from the API.
"""

import requests
from utils.api_client import logger, APIClient


def add_book(api_client: 'APIClient', title: str, book_type: str, creation_date: str) -> requests.Response:
    """
    Adds a new book to the API.

    Args:
        api_client (APIClient): The API client to interact with the Books API.
        title (str): The title of the book.
        book_type (str): The type of the book.
        creation_date (str): The creation date of the book.

    Returns:
        requests.Response: The response object from the API request.
    """
    new_book = {
        'title': title,
        'type': book_type,
        'creation_date': creation_date
    }
    response = api_client.post('manipulation', json=new_book)
    response.raise_for_status()
    return response


def delete_book(api_client: 'APIClient', book_id: str) -> requests.Response:
    """
    Deletes a book from the API by ID.

    Args:
        api_client (APIClient): The API client to interact with the Books API.
        book_id (str): The ID of the book to delete.

    Returns:
        requests.Response: The response object from the API request.
    """
    response = api_client.delete('manipulation', params={'id': book_id})
    response.raise_for_status()
    return response


def update_book(api_client: 'APIClient', book_id: str, title: str) -> requests.Response:
    """
    Updates the title of a book in the API by ID.

    Args:
        api_client (APIClient): The API client to interact with the Books API.
        book_id (str): The ID of the book to update.
        title (str): The new title of the book.

    Returns:
        requests.Response: The response object from the API request.
    """
    response = api_client.put('manipulation', params={'id': book_id}, json={'title': title})
    response.raise_for_status()
    return response


def get_latest_books(api_client: 'APIClient', limit: int) -> requests.Response:
    """
    Retrieves the latest books from the API.

    Args:
        api_client (APIClient): The API client to interact with the Books API.
        limit (int): The number of latest books to retrieve.

    Returns:
        requests.Response: The response object from the API request.
    """
    response = api_client.get('latest', params={'limit': limit})
    response.raise_for_status()
    return response


def get_books_by_type(api_client: 'APIClient', book_type: str) -> requests.Response:
    """
    Retrieves books by type from the API.

    Args:
        api_client (APIClient): The API client to interact with the Books API.
        book_type (str): The type of books to retrieve.

    Returns:
        requests.Response: The response object from the API request.
    """
    response = api_client.get('ids', params={'book_type': book_type})
    response.raise_for_status()
    return response


def get_book_info(api_client: 'APIClient', book_id: str) -> requests.Response:
    """
    Retrieves information about a specific book by ID from the API.

    Args:
        api_client (APIClient): The API client to interact with the Books API.
        book_id (str): The ID of the book to retrieve information for.

    Returns:
        requests.Response: The response object from the API request.
    """
    response = api_client.get('info', params={'id': book_id})
    response.raise_for_status()
    return response


def get_all_books(api_client: 'APIClient') -> list:
    """
    Retrieves all books from the API.

    Args:
        api_client (APIClient): The API client to interact with the Books API.

    Returns:
        list of dict: A list of dictionaries where each dictionary contains the details of a book.
    """
    all_books_ids = []
    book_types = ['Science', 'Satire', 'Drama', 'Romance']  # Add all possible book types here
    for book_type in book_types:
        response = api_client.get('ids', params={'book_type': book_type})
        response.raise_for_status()
        all_books_ids.extend(response.json())
    return all_books_ids


def remove_all_books(api_client: 'APIClient'):
    """
    Removes all books from the API.

    Args:
        api_client (APIClient): The API client to interact with the Books API.
    """
    all_books_ids = get_all_books(api_client)
    for book in all_books_ids:
        try:
            delete_book(api_client, book['id'])
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to delete book with ID {book['id']}: {e}")
