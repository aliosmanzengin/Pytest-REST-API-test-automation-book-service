import uuid


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
    response = api_client.get('ids', params={})
    response.raise_for_status()
    return response.json()


def remove_all_books(api_client):
    all_books_ids = get_all_books(api_client)
    for book in all_books_ids:
        delete_book(api_client, book[id])
