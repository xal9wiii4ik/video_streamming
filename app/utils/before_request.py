import jwt

from flask import request

from models import Account
from settings import TOKEN_TYPE, SECRET_KEY, TOKEN_ALGORITHM
from utils.exceptions import EmptyBodyException, SerializerValidationError


def authenticate() -> None:
    """
    Decorator for authenticate user(set current user to request)
    """

    if request.headers.get('Authorization') is None:
        request.user = None    # type: ignore
    else:
        token_components = request.headers.get("Authorization").split(' ')  # type: ignore
        token_type = token_components[0]
        access_token = token_components[-1]

        if token_type != TOKEN_TYPE:
            raise SerializerValidationError({'token': 'Invalid token type'})

        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[TOKEN_ALGORITHM])  # type: ignore
            if payload['sub'] != 'access':
                raise SerializerValidationError({'error': 'Access token is expected'})
            account = Account.query.filter_by(username=payload['username']).first()
            request.user = account  # type: ignore
        except Exception:
            raise SerializerValidationError({'error': 'Invalid token or token is expired'})


def validate_body_for_update_create() -> None:
    from flask import request

    methods = ['POST', 'PATCH', 'PUT']

    if request.method in methods and request.json is None and not any(request.form) and not any(request.files):
        raise EmptyBodyException('Body for this method cannot be empty')
