import typing as tp
import json


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
