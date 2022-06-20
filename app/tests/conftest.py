import json
import pytest
import settings
import typing as tp

from models import Account, Video

from main import register_flask_application, db

from utils.data_process import make_password


@pytest.fixture(scope='class', autouse=True)
def setup() -> tp.Any:
    app_1 = register_flask_application(settings.TESTING_CONFIGURATION)
    app_1.app_context().push()
    db.init_app(app_1)
    db.create_all()

    password = make_password(password='password')

    account_1 = Account(username='username',
                        password=password,
                        is_staff=False,
                        email='email_example@mail.ru',
                        first_name='first_name',
                        last_name='last_name')
    account_2 = Account(username='username_2',
                        password=password,
                        is_staff=False,
                        email='email_example2@mail.ru',
                        first_name='first_name2',
                        last_name='last_name2')

    video_1 = Video(title='title_1',
                    description='description_1',
                    bucket_path='bucket_path_1',
                    account=account_1,
                    account_id=1)
    video_2 = Video(title='title_2',
                    description='description_2',
                    bucket_path='bucket_path_2',
                    account=account_2,
                    account_id=2)

    db.session.add(account_1)
    db.session.add(account_2)
    db.session.add(video_1)
    db.session.add(video_2)
    db.session.commit()
    yield app_1
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='class', autouse=True)
def setup_token_1(setup: tp.Any) -> tp.Any:
    """
    Setup token data
    """

    data = {
        'username': 'username',
        'password': 'password'
    }
    json_data = json.dumps(data)

    response = setup.test_client().post('/auth/token/', data=json_data, headers={'Content-Type': 'application/json'})
    yield response.json['access_token']


@pytest.fixture(scope='class', autouse=True)
def setup_token_2(setup: tp.Any) -> tp.Any:
    """
    Setup token data
    """

    data = {
        'username': 'username_2',
        'password': 'password'
    }
    json_data = json.dumps(data)

    response = setup.test_client().post('/auth/token/', data=json_data, headers={'Content-Type': 'application/json'})
    yield response.json['access_token']
