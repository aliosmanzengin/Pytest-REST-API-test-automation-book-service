"""
helpers.py
"""
import requests

from utils.api_client import logger


def add_book(api_client, title, book_type, creation_date):
    new_book = {
        'title': title,
        'type': book_type,
        'creation_date': creation_date
    }
    response = api_client.post('manipulation', json=new_book)
    response.raise_for_status()
    return response


def delete_book(api_client, book_id):
    response = api_client.delete('manipulation', params={'id': book_id})
    response.raise_for_status()
    return response


def update_book(api_client, book_id, title):
    response = api_client.put('manipulation', params={'id': book_id}, json={'title': title})
    response.raise_for_status()
    return response


def get_latest_books(api_client, limit):
    response = api_client.get('latest', params={'limit': limit})
    response.raise_for_status()
    return response


def get_books_by_type(api_client, book_type):
    response = api_client.get('ids', params={'book_type': book_type})
    response.raise_for_status()
    return response


def get_book_info(api_client, book_id):
    response = api_client.get('info', params={'id': book_id})
    response.raise_for_status()
    return response


def get_all_books(api_client):
    all_books_ids = []
    book_types = ['Science', 'Satire', 'Drama', 'Romance']  # Add all possible book types here
    for book_type in book_types:
        response = api_client.get('ids', params={'book_type': book_type})
        response.raise_for_status()
        all_books_ids.extend(response.json())
    return all_books_ids


def remove_all_books(api_client):
    all_books_ids = get_all_books(api_client)
    for book in all_books_ids:
        try:
            delete_book(api_client, book['id'])
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to delete book with ID {book['id']}: {e}")