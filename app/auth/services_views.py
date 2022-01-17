import typing as tp
from functools import wraps

import jwt

from datetime import timedelta, datetime

from account.schemas import RegisterUser

from settings import (
    SECRET_KEY,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ACCESS_TOKEN_JWT_SUBJECT,
    TOKEN_TYPE,
    TOKEN_ALGORITHM,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_JWT_SUBJECT,
    DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES,
    DEFAULT_REFRESH_TOKEN_EXPIRE_MINUTES,
)


def create_new_account(data: RegisterUser) -> tp.Dict[str, tp.Union[str, bool]]:
    """
    Create new account
    Args:
        data: register data
    Return:
        dict with account data
    """

    from main import db
    from models import Account

    new_account = Account(username=data.username,
                          password=data.password,
                          is_staff=False,
                          email=data.email,
                          first_name=data.first_name,
                          last_name=data.last_name)
    db.session.add(new_account)
    db.session.commit()
    account_data = data.__dict__
    account_data['id'] = new_account.id
    return account_data


def create_tokens(data: tp.Dict[str, str]) -> tp.Dict[str, str]:
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


def create_token(token_type: str, data: tp.Dict[str, str]) -> str:
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


def generate_access_token_from_refresh(refresh_token: str) -> tp.Tuple[tp.Dict[str, str], int]:
    """
    Generate access token from refresh token
    Args:
        refresh_token: refresh_token
    Return:
        dict with access token and current status code
    """

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[TOKEN_ALGORITHM])

        if payload['sub'] != 'refresh':
            return {'error': 'Refresh token is expected'}, 401

        return_data = create_tokens(data={
            'username': payload["username"],
            'password': payload["password"]
        })
        return return_data, 200
    except Exception:
        return {'error': 'Invalid token or token is expired'}, 401


def authenticate(func: tp.Any) -> tp.Any:
    """
    Decorator for authenticate user(set current user to request)
    """

    from flask import request, jsonify

    @wraps(func)
    def wrapper(*args: tp.Any, **kwargs: tp.Any) -> tp.Any:
        from models import Account
        if request.headers.get('Authorization') is None:
            return jsonify({'error': 'Login required'})

        token_components = request.headers.get("Authorization").split(' ')  # type: ignore
        token_type = token_components[0]
        access_token = token_components[-1]

        if token_type != TOKEN_TYPE:
            return jsonify({'error': 'Invalid token type'})

        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
            if payload['sub'] != 'access':
                return {'error': 'Access token is expected'}, 401
            account = Account.query.filter_by(username=payload['username']).first()
            request.user = account  # type: ignore
        except Exception:
            return {'error': 'Invalid token or token is expired'}, 401
        return func(*args, **kwargs)

    return wrapper
