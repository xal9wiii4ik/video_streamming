import typing as tp

from pydantic import root_validator

from models import Account

from utils.exceptions import SerializerValidationError
from utils.serializers import BaseSerializer, serializer_data_type
from utils.data_process import make_password


class AccessTokenSerializer(BaseSerializer):
    """
    Serializer for access token
    """

    read_only_fields = ['user_pk']

    username: str
    password: str
    user_pk: tp.Optional[int] = None

    @root_validator
    def validate_all_values(cls, data: serializer_data_type) -> serializer_data_type:
        """
        Validate all values
        """

        accounts = Account.query.filter_by(username=data.get('username')).all()
        if not accounts:
            raise SerializerValidationError({'error': 'Account does not exist'})

        account = accounts[0]
        account_password = account.password
        data['user_pk'] = account.id

        password = make_password(password=data.get('password'))
        if password != account_password:
            raise SerializerValidationError({'error': 'Invalid password'})
        return data


class RefreshTokenSerializer(BaseSerializer):
    """
    Serializer for access token
    """

    refresh_token: str
