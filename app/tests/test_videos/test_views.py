import typing as tp


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


def test_get_videos_pagination(setup: tp.Any, setup_token_1: tp.Any) -> None:
    """
    Test get videos with pagination
    """

    response_1 = setup.test_client().get('/api/video/?limit=1&offset=0', headers={
        'Authorization': f'Token {setup_token_1}'
    })
    response_data_1 = response_1.json
    for data in response_data_1:
        del data['upload_time']
    expected_data_1 = [
        {
            'account_id': 2,
            'bucket_path': 'bucket_path_2',
            'description': 'description_2',
            'id': 2,
            'title': 'title_2',
            'username': 'username_2'
        }
    ]
    assert response_data_1 == expected_data_1
    assert response_1.status_code == 200
    response_2 = setup.test_client().get('/api/video/?limit=1&offset=1', headers={
        'Authorization': f'Token {setup_token_1}'
    })
    response_data_2 = response_2.json
    for data in response_data_2:
        del data['upload_time']
    expected_data_2 = [
        {
            'account_id': 1,
            'bucket_path': 'bucket_path_1',
            'description': 'description_1',
            'id': 1,
            'title': 'title_1',
            'username': 'username'
        }
    ]
    assert response_data_2 == expected_data_2
    assert response_2.status_code == 200


def test_get_videos_sort(setup: tp.Any, setup_token_1: tp.Any) -> None:
    """
    Test get videos with sorting
    """

    response_1 = setup.test_client().get('/api/video/?sort=id&sort_type=asc&limit=1&offset=0', headers={
        'Authorization': f'Token {setup_token_1}'
    })
    response_data_1 = response_1.json
    for data in response_data_1:
        del data['upload_time']
    expected_data_1 = [
        {
            'account_id': 1,
            'bucket_path': 'bucket_path_1',
            'description': 'description_1',
            'id': 1,
            'title': 'title_1',
            'username': 'username'
        }
    ]
    print(response_data_1)
    assert response_data_1 == expected_data_1
    assert response_1.status_code == 200

    response_2 = setup.test_client().get('/api/video/?sort=id&sort_type=desc&limit=1&offset=0', headers={
        'Authorization': f'Token {setup_token_1}'
    })
    response_data_2 = response_2.json
    for data in response_data_2:
        del data['upload_time']
    expected_data_2 = [
        {
            'account_id': 2,
            'bucket_path': 'bucket_path_2',
            'description': 'description_2',
            'id': 2,
            'title': 'title_2',
            'username': 'username_2'
        }
    ]
    assert response_data_2 == expected_data_2
    assert response_2.status_code == 200


def test_get_videos_search(setup: tp.Any, setup_token_1: tp.Any) -> None:
    """
    Test get videos with search
    """

    response = setup.test_client().get('/api/video/?search=title_1', headers={
        'Authorization': f'Token {setup_token_1}'
    })
    response_data = response.json
    for data in response_data:
        del data['upload_time']
    expected_data = [
        {
            'account_id': 1,
            'bucket_path': 'bucket_path_1',
            'description': 'description_1',
            'id': 1,
            'title': 'title_1',
            'username': 'username'
        }
    ]
    assert response_data == expected_data
    assert response.status_code == 200

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
