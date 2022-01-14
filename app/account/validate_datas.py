import typing as tp

from account.schemas import RegisterUser, AccessToken
from utils.data_process import make_password


def validate_register_account_data(data: RegisterUser) -> tp.Tuple[tp.Union[RegisterUser, tp.Dict[str, str]], int]:
    """
    Validate register user data
    Args:
        data: data
    Returns:
        Error message or success data with code
    """

    from models import Account

    # validate password
    if data.password != data.repeat_password:
        return {'ValidationError': 'Password should be equal to repeat password'}, 400
    if len(data.password) < 8:
        return {'ValidationError': 'Password must be more than 8 characters'}, 400
    password = make_password(data.password)
    data.password = password

    # validate username
    accounts = Account.query.filter_by(username=data.username).all()
    if any(accounts):
        return {'ValidationError': 'Account with this username already exist'}, 400

    # validate email value
    if data.email.find('@') == -1 or data.email.find('.') == -1:
        return {'ValidationError': 'Invalid email'}, 400

    # validate email
    accounts = Account.query.filter_by(email=data.email).all()
    if any(accounts):
        return {'ValidationError': 'Account with this email already exist'}, 400

    return data, 200


def validate_access_token_data(data: AccessToken) -> tp.Tuple[tp.Union[AccessToken, tp.Dict[str, str]], int]:
    """
    Validate access token data
    Args:
        data: token data
    Returns:
        Error message or success data with code
    """

    from models import Account

    accounts = Account.query.filter_by(username=data.username).all()
    if not any(accounts):
        return {'ValidationError': 'Account does not exist'}, 400

    account = accounts[0]
    account_password = account.password
    data.user_pk = account.id

    password = make_password(password=data.password)
    if password != account_password:
        return {'ValidationError': 'Invalid password'}, 400
    return data, 200
