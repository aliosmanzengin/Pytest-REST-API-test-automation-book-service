# tests/test_booking_api.py
import pytest
import allure
from assertpy import assert_that
from datetime import datetime
import uuid
import requests.exceptions  # This is the required import

from tests.helpers import add_book, delete_book, update_book, get_latest_books, get_book_info, get_books_by_type


@allure.feature('Books API')
class TestBooksAPI:

    @allure.story('Add Book')
    def test_add_new_book(self, api_client):
        response = add_book(api_client, 'Book1', 'Satire', '2021-01-02')
        assert_that(response.status_code).is_equal_to(200)
        response_json = response.json()
        assert_that(response_json['title']).is_equal_to('Book1')
        assert_that(response_json['type']).is_equal_to('Satire')
        assert_that(response_json['creation_date']).is_equal_to('2021-01-02')
        assert_that(response_json['id']).is_not_empty()

    @allure.story('Delete Book')
    def test_delete_book(self, api_client):
        add_response = add_book(api_client, 'BookToDelete', 'Drama', '2021-02-02')
        assert_that(add_response.status_code).is_equal_to(200)

        book_id = add_response.json()['id']
        book_title = add_response.json()['title']

        delete_response = delete_book(api_client, book_id)
        assert_that(delete_response.status_code).is_equal_to(200)
        assert_that(delete_response.json()['id']).is_equal_to(book_id)
        assert_that(delete_response.json()['title']).is_equal_to(book_title)

    @allure.story('Update Book')
    def test_update_book(self, api_client):
        add_response = add_book(api_client, 'BookToUpdate', 'Science', '2021-03-03')
        assert_that(add_response.status_code).is_equal_to(200)

        book_id = add_response.json()['id']

        updated_title = 'UpdatedBookTitle'
        update_response = update_book(api_client, book_id, updated_title)

        assert_that(update_response.status_code).is_equal_to(200)
        response_data = update_response.json()
        assert_that(response_data['title']).is_equal_to(updated_title)
        assert_that(response_data['updated_date_time']).is_not_none()

    @allure.story('Get Latest Books')
    @pytest.mark.parametrize('limit', [1, 5, 10])
    def test_get_latest_books(self, api_client, limit):
        response = get_latest_books(api_client, limit)
        assert_that(response.status_code).is_equal_to(200)
        response_data = response.json()
        assert_that(response_data).is_instance_of(list)
        assert_that(len(response_data)).is_less_than_or_equal_to(limit)

    @allure.story('Get Book Info')
    def test_get_book_info(self, api_client):
        add_response = add_book(api_client, 'MyBook1', 'Science', '2021-03-03')
        assert_that(add_response.status_code).is_equal_to(200)
        book_id = add_response.json()['id']

        response = get_book_info(api_client, book_id)

        assert_that(response.status_code).is_equal_to(200)
        response_data = response.json()
        assert_that(response_data['id']).is_equal_to(book_id)
        assert_that(response_data['title']).is_equal_to('MyBook1')
        assert_that(response_data['type']).is_equal_to('Science')

    @allure.story('Get Book IDs by Type')
    @pytest.mark.parametrize('book_type', ['Science', 'Satire', 'Drama', 'Romance'])
    def test_get_book_ids_by_type(self, api_client, book_type):
        response = get_books_by_type(api_client, book_type)
        assert_that(response.status_code).is_equal_to(200)

        response_data = response.json()
        assert_that(response_data).is_instance_of(list)
        for book in response_data:
            assert_that(uuid.UUID(book['id'], version=4)).is_instance_of(uuid.UUID)

    @allure.story('Add Book Missing Field')
    def test_add_book_missing_field(self, api_client):
        new_book = {
            'title': 'BookWithoutType',
            'creation_date': '2021-01-02'
        }
        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            api_client.post('manipulation', json=new_book)

        response = exc_info.value.response
        assert_that(response.status_code).is_equal_to(400)
        assert_that(response.json()['message']).is_equal_to('The request is not valid.')

    @allure.story('Delete Non-existent Book')
    def test_delete_non_existent_book(self, api_client):
        book_id = str(uuid.uuid4())
        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            api_client.delete('manipulation', params={'id': book_id})

        response = exc_info.value.response
        assert_that(response.status_code).is_equal_to(404)
        assert_that(response.json()['message']).is_equal_to('There is no such book | books.')

    @allure.story('Update Non-existent Book')
    def test_update_non_existent_book(self, api_client):
        book_id = str(uuid.uuid4())
        updated_title = 'NonExistentBookTitle'

        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            api_client.put('manipulation', params={'id': book_id}, json={'title': updated_title})

        response = exc_info.value.response
        assert_that(response.json()['message']).contains('There is no such book | books.')
        assert_that(response.status_code).is_equal_to(404)

    @allure.story('Get Info of Non-existent Book')
    def test_get_info_non_existent_book(self, api_client):
        book_id = str(uuid.uuid4())
        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            api_client.get('info', params={'id': book_id})

        response = exc_info.value.response
        assert_that(response.status_code).is_equal_to(404)
        assert_that(response.json()['message']).is_equal_to('There is no such book | books.')

    @allure.story('Get Book IDs with Invalid Type')
    def test_get_book_ids_invalid_type(self, api_client):
        invalid_book_type = 'NonExistentType'
        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            api_client.get('ids', params={'book_type': invalid_book_type})

        response = exc_info.value.response
        assert_that(response.status_code).is_equal_to(400)
        assert_that(response.json()['message']).is_equal_to('The book entity is not valid.')
