import pytest
from flask import Flask

from account.models import Account
from account.schemas import RegisterUser
from account.validate_datas import validate_register_account_data
from main import register_flask_application, db, app


class TestValidateRegisterAccountData:
    """
    Test func validate_register_account_data
    """

    @pytest.fixture(scope='class', autouse=True)
    def setup(self) -> Flask:
        app_1 = register_flask_application()
        app_1.app_context().push()
        db.init_app(app_1)
        db.create_all()
        new_account = Account(username='username',
                              password='password',
                              is_staff=False,
                              email='email_example@mail.ru',
                              first_name='first_name',
                              last_name='last_name')
        db.session.add(new_account)
        db.session.commit()
        return app

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

    # def test_exist_username(self) -> None:
    #     """
    #     Test case exist username
    #     """

        # data = RegisterUser(password='123',
        #                     repeat_password='123',
        #                     email='123',
        #                     username='username_1',
        #                     first_name='123',
        #                     last_name='123')
        # return_data, status_code = validate_register_account_data(data=data)
        # assert status_code == 400
        # assert True
