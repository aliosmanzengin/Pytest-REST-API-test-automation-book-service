# tests/test_booking_api.py
import pytest
import allure

@allure.feature('User API')
@allure.story('Get User Information')
@pytest.mark.parametrize('user_id, expected_name', [
    (1, 'John Doe'),
    (2, 'Jane Doe')
])
def test_get_user(api_client, user_id, expected_name):
    response = api_client.get(f'user/{user_id}')
    assert response['id'] == user_id
    assert response['name'] == expected_name

@allure.feature('User API')
@allure.story('Create User')
def test_create_user(api_client):
    new_user = {
        'name': 'Jane Doe',
        'email': 'jane.doe@example.com'
    }
    response = api_client.post('user', json=new_user)
    assert response['name'] == new_user['name']
    assert response['email'] == new_user['email']
