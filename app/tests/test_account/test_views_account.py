import json
import typing as tp

from tests.setup_tests import *


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
    Test update user
    """

    response = setup.test_client().get('/api/account/', headers={
        'Authorization': f'Token {setup_token_1}'
    })
    assert response.status_code == 200
