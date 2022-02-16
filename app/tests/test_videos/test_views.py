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
