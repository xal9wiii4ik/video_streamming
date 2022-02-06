import typing as tp

import jwt

from datetime import timedelta, datetime

from settings import (
    SECRET_KEY,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ACCESS_TOKEN_JWT_SUBJECT,
    TOKEN_ALGORITHM,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_JWT_SUBJECT,
    DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES,
    DEFAULT_REFRESH_TOKEN_EXPIRE_MINUTES,
)
from utils.exceptions import SerializerValidationError
from utils.serializers import serializer_data_type


def create_tokens(data: serializer_data_type) -> tp.Dict[str, str]:
    """
    Create tokens
    Args:
        data: dict with username and password
    Return:
        dict with access and refresh token
    """

    access_token = create_token(token_type='access', data=data.copy())
    refresh_token = create_token(token_type='refresh', data=data.copy())
    return_data = ({'refresh_token': refresh_token, 'access_token': access_token})

    return return_data


def create_token(token_type: str, data: serializer_data_type) -> str:
    """
    Create access token using credentials or refresh token
    Args:
        token_type: access or refresh
        data: user credentials
    Returns:
        new token
    """

    helping_data: tp.Any = {
        'refresh': {
            'expire': REFRESH_TOKEN_EXPIRE_MINUTES,
            'default_expire': DEFAULT_REFRESH_TOKEN_EXPIRE_MINUTES,
            'subject': REFRESH_TOKEN_JWT_SUBJECT
        },
        'access': {
            'expire': ACCESS_TOKEN_EXPIRE_MINUTES,
            'default_expire': DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES,
            'subject': ACCESS_TOKEN_JWT_SUBJECT
        }
    }

    if helping_data[token_type]['expire'] is not None:
        helping_data['expire'] = datetime.utcnow() + timedelta(minutes=float(helping_data[token_type]['expire']))
    else:
        helping_data['expire'] = datetime.utcnow() + timedelta(
            minutes=float(helping_data[token_type]['default_expire'])
        )

    data.update({'exp': helping_data['expire'], 'sub': helping_data[token_type]['subject']})
    encoded_jwt: str = jwt.encode(payload=data, key=SECRET_KEY, algorithm=TOKEN_ALGORITHM)
    return encoded_jwt


def generate_access_token_from_refresh(refresh_token: str) -> tp.Dict[str, str]:
    """
    Generate access token from refresh token
    Args:
        refresh_token: refresh_token
    Return:
        dict with access token
    """

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[TOKEN_ALGORITHM])

        if payload['sub'] != 'refresh':
            raise SerializerValidationError({'token': 'Refresh token is expected'})

        return_data = create_tokens(data={
            'username': payload["username"],
            'password': payload["password"]
        })
        return return_data
    except Exception:
        raise SerializerValidationError({'token': 'Invalid token or token is expired'})
