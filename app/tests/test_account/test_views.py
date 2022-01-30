import typing as tp
import json

from tests.setup_tests import *


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


def test_get_user(setup: tp.Any, setup_token_1: tp.Any) -> None:
    """
    Test get user
    """

    response = setup.test_client().get('/api/account/1/', headers={
        'Authorization': f'Token {setup_token_1}'
    })
    assert response.status_code == 200


def test_get_user_not_found(setup: tp.Any, setup_token_1: tp.Any) -> None:
    """
    Test get user not found
    """

    response = setup.test_client().get('/api/account/100/', headers={
        'Authorization': f'Token {setup_token_1}'
    })
    assert response.status_code == 404


def test_delete_user_owner(setup: tp.Any, setup_token_1: tp.Any) -> None:
    """
    Test delete user owner
    """

    response = setup.test_client().delete('/api/account/1/', headers={
        'Authorization': f'Token {setup_token_1}'
    })
    assert response.status_code == 204


def test_delete_user_not_owner(setup: tp.Any, setup_token_2: tp.Any) -> None:
    """
    Test delete user not owner
    """

    response = setup.test_client().delete('/api/account/1/', headers={
        'Authorization': f'Token {setup_token_2}'
    })
    assert response.status_code == 401


def test_update_user(setup: tp.Any, setup_token_1: tp.Any) -> None:
    """
    Test update user
    """

    data = {
        'first_name': 'Nikita'
    }
    json_data = json.dumps(data)

    response = setup.test_client().patch('/api/account/1/', data=json_data, headers={
        'Authorization': f'Token {setup_token_1}',
        'Content-Type': 'application/json'
    })
    assert response.status_code == 200


def test_update_user_not_owner(setup: tp.Any, setup_token_2: tp.Any) -> None:
    """
    Test update user not owner
    """

    data = {
        'first_name': 'Nikita'
    }
    json_data = json.dumps(data)

    response = setup.test_client().patch('/api/account/1/', data=json_data, headers={
        'Authorization': f'Token {setup_token_2}',
        'Content-Type': 'application/json'
    })
    assert response.status_code == 401


def test_get_users(setup: tp.Any, setup_token_1: tp.Any) -> None:
    """
    Test get users
    """

    response = setup.test_client().get('/api/account/', headers={
        'Authorization': f'Token {setup_token_1}'
    })
    assert response.status_code == 200
