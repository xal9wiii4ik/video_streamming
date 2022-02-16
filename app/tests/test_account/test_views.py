import typing as tp
import json


def test_user_register(setup: tp.Any) -> None:
    """
    Test user register view
    """

    data = {
        'username': 'xal9',
        'password': '123456789',
        'repeat_password': '123456789',
        'email': 'email@mail.ru',
        'first_name': 'first_name',
        'last_name': 'first_name'
    }
    json_data = json.dumps(data)

    response = setup.test_client().post('/api/account/register/',
                                        data=json_data,
                                        headers={'Content-Type': 'application/json'})
    assert response.status_code == 200


def test_user_register_invalid_password(setup: tp.Any) -> None:
    """
    Test user register view invalid password
    """

    data = {
        'username': 'xal9',
        'password': '123',
        'repeat_password': '123',
        'email': 'email@mail.ru',
        'first_name': 'first_name',
        'last_name': 'first_name'
    }
    json_data = json.dumps(data)

    response = setup.test_client().post('/api/account/register/',
                                        data=json_data,
                                        headers={'Content-Type': 'application/json'})
    assert response.status_code == 400


def test_user_register_invalid_repeat_password(setup: tp.Any) -> None:
    """
    Test user register view invalid repeat password
    """

    data = {
        'username': 'xal9',
        'password': '123456789',
        'repeat_password': '123',
        'email': 'email@mail.ru',
        'first_name': 'first_name',
        'last_name': 'first_name'
    }
    json_data = json.dumps(data)

    response = setup.test_client().post(
        '/api/account/register/',
        data=json_data,
        headers={'Content-Type': 'application/json'})
    assert response.status_code == 400


def test_user_register_invalid_username(setup: tp.Any) -> None:
    """
    Test user register view invalid username
    """

    data = {
        'username': 'username',
        'password': '123456789',
        'repeat_password': '123456789',
        'email': 'email@mail.ru',
        'first_name': 'first_name',
        'last_name': 'first_name'
    }
    json_data = json.dumps(data)

    response = setup.test_client().post(
        '/api/account/register/',
        data=json_data,
        headers={'Content-Type': 'application/json'})
    assert response.status_code == 400


def test_user_register_invalid_email(setup: tp.Any) -> None:
    """
    Test user register view invalid email
    """

    data = {
        'username': 'username',
        'password': '123456789',
        'repeat_password': '123456789',
        'email': 'email_example@mail.ru',
        'first_name': 'first_name',
        'last_name': 'first_name'
    }
    json_data = json.dumps(data)

    response = setup.test_client().post(
        '/api/account/register/',
        data=json_data,
        headers={'Content-Type': 'application/json'})
    assert response.status_code == 400


def test_get_users(setup: tp.Any, setup_token_1: tp.Any) -> None:
    """
    Test get users
    """

    response = setup.test_client().get('/api/account/', headers={
        'Authorization': f'Token {setup_token_1}'
    })
    assert response.status_code == 200
    expected_data = [
        {
            'email': 'email_example2@mail.ru',
            'first_name': 'first_name2',
            'id': 2,
            'is_staff': False,
            'last_name': 'last_name2',
            'username': 'username_2'
        },
        {
            'email': 'email_example@mail.ru',
            'first_name': 'first_name',
            'id': 1,
            'is_staff': False,
            'last_name': 'last_name',
            'username': 'username'
        }
    ]
    assert expected_data == response.json
