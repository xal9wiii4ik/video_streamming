import json
import typing as tp

from tests.setup_tests import *


def test_user_register(setup: tp.Any) -> None:
    """
    Test user register view
    """

    data = {
        'username': 'xal9',
        'password': '12345678',
        'repeat_password': '12345678',
        'email': 'email@mail.ru',
        'first_name': 'first_name',
        'last_name': 'first_name'
    }
    json_data = json.dumps(data)

    response = setup.test_client().post('/auth/register/', data=json_data, headers={'Content-Type': 'application/json'})
    assert response.status_code == 200


def test_tokens(setup: tp.Any) -> None:
    """
    Test get tokens and refresh token
    """

    data = {
        'username': 'username',
        'password': 'password'
    }
    json_data = json.dumps(data)

    response = setup.test_client().post('/auth/token/', data=json_data, headers={'Content-Type': 'application/json'})
    assert response.status_code == 200

    data_1 = {
        'refresh_token': response.json.get('refresh_token')
    }
    json_data_1 = json.dumps(data_1)
    response_1 = setup.test_client().post(
        '/auth/token_refresh/',
        data=json_data_1,
        headers={'Content-Type': 'application/json'}
    )
    assert response_1.status_code == 200
