# tests/test_booking_api.py
import pytest
import allure
from assertpy import assert_that
from datetime import datetime
import uuid


@allure.feature('Books API')
class TestBooksAPI:

    @allure.story('Add Book')
    def test_add_book(self, api_client):
        new_book = {
            'title': 'Book1',
            'type': 'Satire',
            'creation_date': '2021-01-02'
        }
        response = api_client.post('manipulation', json=new_book)
        assert_that(response['title']).is_equal_to(new_book['title'])
        assert_that(response['type']).is_equal_to(new_book['type'])
        assert_that(response['creation_date']).is_equal_to(new_book['creation_date'])
        self.book_id = response['id']  # Store the ID for further tests

    @allure.story('Delete Book')
    def test_delete_book(self, api_client):
        new_book = {
            'title': 'BookToDelete',
            'type': 'Drama',
            'creation_date': '2021-02-02'
        }
        add_response = api_client.post('manipulation', json=new_book)
        book_id = add_response['id']
        delete_response = api_client.delete('manipulation', params={'id': book_id})
        assert_that(delete_response['message']).is_equal_to('Book deleted')

    @allure.story('Update Book')
    def test_update_book(self, api_client):
        new_book = {
            'title': 'BookToUpdate',
            'type': 'Action and Adventure',
            'creation_date': '2021-03-03'
        }
        add_response = api_client.post('manipulation', json=new_book)
        book_id = add_response['id']
        updated_title = 'UpdatedBookTitle'
        update_response = api_client.put('manipulation', json={'id': book_id, 'title': updated_title})
        assert_that(update_response['title']).is_equal_to(updated_title)
        assert_that(update_response['updated_date']).is_not_none()

    @allure.story('Get Latest Books')
    @pytest.mark.parametrize('limit', [1, 5, 10])
    def test_get_latest_books(self, api_client, limit):
        response = api_client.get('latest', params={'limit': limit})
        assert_that(response).is_instance_of(list)
        assert_that(len(response)).is_less_than_or_equal_to(limit)

    @allure.story('Get Book Info')
    def test_get_book_info(self, api_client):
        new_book = {
            'title': 'BookInfo',
            'type': 'Romance',
            'creation_date': '2021-04-04'
        }
        add_response = api_client.post('manipulation', json=new_book)
        book_id = add_response['id']
        response = api_client.get('info', params={'id': book_id})
        assert_that(response['id']).is_equal_to(book_id)
        assert_that(response['title']).is_equal_to(new_book['title'])
        assert_that(response['type']).is_equal_to(new_book['type'])

    @allure.story('Get Book IDs by Type')
    @pytest.mark.parametrize('book_type', ['Science', 'Satire', 'Drama', 'Action and Adventure', 'Romance'])
    def test_get_book_ids_by_type(self, api_client, book_type):
        response = api_client.get('ids', params={'book_type': book_type})
        assert_that(response).is_instance_of(list)
        for book_id in response:
            assert_that(uuid.UUID(book_id, version=4)).is_instance_of(uuid.UUID)  # Ensure IDs are valid UUIDs
