from pydantic import constr, validator, root_validator

from sqlalchemy import exists

from models import Account, db

from utils.exceptions import SerializerValidationError
from utils.serializers import BaseSerializer, BaseModelSerializer, serializer_data_type
from utils.data_process import make_password


def validate_email(email: str) -> str:
    """
    Help function for validating email
    Args:
        email: current email
    Returns:
         email
    """

    if '@' not in email or '.' not in email:
        raise ValueError('Invalid email')

    is_exist = db.session().query(exists().where(Account.username == email)).scalar()
    if is_exist:
        raise SerializerValidationError({'error': 'Account with this email already exist'})

    return email


class RegisterUserSerializer(BaseSerializer):
    """ Serializer for register users """

    write_only_fields = ['password', 'repeat_password']

    username: constr(max_length=100)  # type: ignore
    password: constr(max_length=500)  # type: ignore
    repeat_password: constr(max_length=500)  # type: ignore
    email: constr(max_length=100)  # type: ignore
    first_name: constr(max_length=100)  # type: ignore
    last_name: constr(max_length=100)  # type: ignore

    @validator('username')
    def validate_username(cls, username: str) -> str:
        is_exist = db.session().query(exists().where(Account.username == username)).scalar()
        if is_exist:
            raise SerializerValidationError({'error': 'Account with this username already exist'})
        return username

    @validator('email')
    def validate_email(cls, email: str) -> str:
        return validate_email(email=email)

    @root_validator(pre=True)
    def validate_all_values(cls, data: serializer_data_type) -> serializer_data_type:
        """
        Validate all values
        """

        if len(data['password']) <= 8:
            raise SerializerValidationError({'error': 'Password must be more than 8 characters'})

        if data['password'] != data['repeat_password']:
            raise SerializerValidationError({'error': 'Password should be equal to repeat password'})

        password = make_password(data['password'])
        data['password'] = password

        return data


class AccountModelSerializer(BaseModelSerializer):
    """
    Model serializer for model account for owner
    """

    read_only_fields = ['id']
    write_only_fields = ['password']
    model = Account

    def validate_email(self, email: str) -> str:
        return validate_email(email=email)

    def validate_password(self, value: str) -> str:
        if len(value) <= 8:
            raise SerializerValidationError({'error': 'Password must be more than 8 characters'})
        return value
