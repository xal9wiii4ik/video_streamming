import typing as tp
import json

from tests.setup_tests import *


def test_get_video(setup: tp.Any, setup_token_1: tp.Any) -> None:
    """
    Test get video
    """

    response = setup.test_client().get('/api/video/1/', headers={
        'Authorization': f'Token {setup_token_1}'
    })
    assert response.status_code == 200
    expected_data = {
        'account_id': 1,
        'bucket_path': 'bucket_path_1',
        'description': 'description_1',
        'id': 1,
        'title': 'title_1',
        'username': 'username'
    }
    response_data = response.json
    del response_data['upload_time']
    assert expected_data == response_data


def test_get_video_not_found(setup: tp.Any, setup_token_1: tp.Any) -> None:
    """
    Test get video not found
    """

    response = setup.test_client().get('/api/video/100/', headers={
        'Authorization': f'Token {setup_token_1}'
    })
    assert response.status_code == 404


# TODO ask or miss this(and create) test case
# def test_delete_video_owner(setup: tp.Any, setup_token_1: tp.Any) -> None:
#     """
#     Test delete video owner
#     """
#
#     response = setup.test_client().delete('/api/video/1/', headers={
#         'Authorization': f'Token {setup_token_1}'
#     })
#     assert response.status_code == 204


def test_delete_video_not_owner(setup: tp.Any, setup_token_2: tp.Any) -> None:
    """
    Test delete video not owner
    """

    response = setup.test_client().delete('/api/video/1/', headers={
        'Authorization': f'Token {setup_token_2}'
    })
    assert response.status_code == 401


def test_update_video(setup: tp.Any, setup_token_1: tp.Any) -> None:
    """
    Test update video
    """

    data = {
        'title': 'new_title_1'
    }
    json_data = json.dumps(data)

    response = setup.test_client().patch('/api/video/1/', data=json_data, headers={
        'Authorization': f'Token {setup_token_1}',
        'Content-Type': 'application/json'
    })
    assert response.status_code == 200


def test_update_video_not_owner(setup: tp.Any, setup_token_2: tp.Any) -> None:
    """
    Test update video not owner
    """

    data = {
        'title': 'new_title_1'
    }
    json_data = json.dumps(data)

    response = setup.test_client().patch('/api/video/1/', data=json_data, headers={
        'Authorization': f'Token {setup_token_2}',
        'Content-Type': 'application/json'
    })
    assert response.status_code == 401


def test_get_videos(setup: tp.Any, setup_token_1: tp.Any) -> None:
    """
    Test get videos
    """

    response = setup.test_client().get('/api/video/', headers={
        'Authorization': f'Token {setup_token_1}'
    })
    assert response.status_code == 200
    expected_data = [
        {
            'account_id': 2,
            'bucket_path': 'bucket_path_2',
            'description': 'description_2',
            'id': 2,
            'title': 'title_2',
            'username': 'username_2'
        },
        {
            'account_id': 1,
            'bucket_path': 'bucket_path_1',
            'description': 'description_1',
            'id': 1,
            'title': 'title_1',
            'username': 'username'
        }
    ]
    response_data = response.json
    for data in response_data:
        del data['upload_time']
    assert expected_data == response_data

# def test_create_video(setup: tp.Any, setup_token_1: tp.Any) -> None:
#     """
#     Test create video
#     """
#
#     data = {
#         'title': 'title_3',
#         'description': 'description_3',
#         'bucket_path': 'bucket_path_3'
#     }
#     json_data = json.dumps(data)
#
#     response = setup.test_client().post('/api/video/', data=json_data, headers={
#         'Authorization': f'Token {setup_token_1}',
#         'Content-Type': 'application/json'
#     })
#     assert response.status_code == 201