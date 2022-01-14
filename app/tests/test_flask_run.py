import typing as tp

from tests.setup_tests import *


def test_index_route(setup: tp.Any) -> None:
    response = setup.test_client().get('/')

    assert response.status_code == 200
    assert response.json == {'ok': 'Main page'}
