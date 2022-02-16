from pydantic import constr, validator, root_validator

from models import Account

from utils.exceptions import SerializerValidationError
from utils.serializers import BaseSerializer, BaseModelSerializer, serializer_data_type
from utils.data_process import make_password


class RegisterUserSerializer(BaseSerializer):
    """ Serializer for register users """

    username: constr(max_length=100)  # type: ignore
    password: constr(max_length=500)  # type: ignore
    repeat_password: constr(max_length=500)  # type: ignore
    email: constr(max_length=100)  # type: ignore
    first_name: constr(max_length=100)  # type: ignore
    last_name: constr(max_length=100)  # type: ignore

    @validator('username')
    def validate_username(cls, value: str) -> str:
        from models import Account

        accounts = Account.query.filter_by(username=value).all()
        if any(accounts):
            raise SerializerValidationError({'error': 'Account with this username already exist'})
        return value

    @validator('email')
    def validate_email(cls, value: str) -> str:
        from models import Account

        if value.find('@') == -1 or value.find('.') == -1:
            raise ValueError('Invalid email')

        accounts = Account.query.filter_by(email=value).all()
        if any(accounts):
            raise SerializerValidationError({'error': 'Account with this email already exist'})

        return value

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

    def validate_email(self, value: str) -> str:
        from models import Account

        if value.find('@') == -1 or value.find('.') == -1:
            raise SerializerValidationError({'error': 'Invalid email'})

        accounts = Account.query.filter_by(email=value).all()
        if any(accounts):
            raise SerializerValidationError({'error': 'Account with this email already exist'})

        return value

    def validate_password(self, value: str) -> str:
        if len(value) <= 8:
            raise SerializerValidationError({'error': 'Password must be more than 8 characters'})
        return value
