import pytest

import settings
import typing as tp

from account.models import Account
from account.schemas import RegisterUser, AccessToken
from account.validate_datas import validate_register_account_data, validate_access_token_data

from main import register_flask_application, db

from utils import make_password


@pytest.fixture(scope='class', autouse=True)
def setup() -> tp.Any:
    app_1 = register_flask_application(settings.TESTING_CONFIGURATION)
    app_1.app_context().push()
    db.init_app(app_1)
    db.create_all()

    password = make_password(password='password')

    account = Account(username='username',
                      password=password,
                      is_staff=False,
                      email='email_example@mail.ru',
                      first_name='first_name',
                      last_name='last_name')

    db.session.add(account)
    db.session.commit()
    yield app_1
    db.session.remove()
    db.drop_all()


class TestValidateRegisterAccountData:
    """
    Test func validate_register_account_data
    """

    def test_not_equal_password_and_repeat_password(self) -> None:
        """
        Test case not equal password and repeat password
        """

        data = RegisterUser(password='123',
                            repeat_password='321',
                            email='123',
                            username='123',
                            first_name='123',
                            last_name='123')
        return_data, status_code = validate_register_account_data(data=data)
        assert status_code == 400
        assert return_data == {'ValidationError': 'Password should be equal to repeat_password'}

    def test_exist_username(self) -> None:
        """
        Test case exist username
        """

        data = RegisterUser(password='123',
                            repeat_password='123',
                            email='123',
                            username='username',
                            first_name='123',
                            last_name='123')
        return_data, status_code = validate_register_account_data(data=data)
        assert status_code == 400
        assert return_data == {'ValidationError': 'Account with this username already exist'}

    def test_invalid_email(self) -> None:
        """
        Test case for invalid email
        """

        data = RegisterUser(password='123',
                            repeat_password='123',
                            email='123',
                            username='123',
                            first_name='123',
                            last_name='123')
        data_1 = RegisterUser(password='123',
                              repeat_password='123',
                              email='123@mailru',
                              username='123',
                              first_name='123',
                              last_name='123')
        return_data, status_code = validate_register_account_data(data=data)
        assert status_code == 400
        assert return_data == {'ValidationError': 'Invalid email'}

        return_data, status_code = validate_register_account_data(data=data_1)
        assert status_code == 400
        assert return_data == {'ValidationError': 'Invalid email'}

    def test_email_exist(self) -> None:
        """
        Test case for invalid email
        """

        data = RegisterUser(password='123',
                            repeat_password='123',
                            email='email_example@mail.ru',
                            username='username_1',
                            first_name='123',
                            last_name='123')
        return_data, status_code = validate_register_account_data(data=data)
        assert status_code == 400
        assert return_data == {'ValidationError': 'Account with this email already exist'}

    def test_valid_data(self) -> None:
        """
        Test case for valid data
        """

        data = RegisterUser(password='123',
                            repeat_password='123',
                            email='new_email@mail.ru',
                            username='new_username',
                            first_name='123',
                            last_name='123')
        return_data, status_code = validate_register_account_data(data=data)
        assert status_code == 200


class TestValidateAccessTokenData:
    """
    Test func validate_register_account_data
    """

    def test_user_does_not_exist(self) -> None:
        """
        Test case for user does not exist
        """

        data = AccessToken(username='123', password=123)
        return_data, status_code = validate_access_token_data(data=data)
        assert status_code == 400
        assert return_data == {'ValidationError': 'Account does not exist'}

    def test_password_not_equal(self) -> None:
        """
        Test case for not equal password
        """

        data = AccessToken(username='username', password='password123')
        return_data, status_code = validate_access_token_data(data=data)
        assert status_code == 400
        assert return_data == {'ValidationError': 'Invalid password'}

    def test_valid_data(self) -> None:
        """
        Test case for valid data
        """

        data = AccessToken(username='username', password='password')
        return_data, status_code = validate_access_token_data(data=data)
        assert status_code == 200
