from main import app


def test_index_route() -> None:
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.json == {'ok': 'Main page'}
