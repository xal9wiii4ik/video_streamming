import typing as tp

from flask import Response, jsonify, request
from flask_pydantic import validate

from account.schemas import RegisterUser, AccessToken, RefreshToken
from account.services_views import create_new_account, create_tokens, generate_access_token_from_refresh, authenticate
from account.validate_datas import validate_register_account_data, validate_access_token_data
from main import app


# TODO add test
@app.route('/api/register/', methods=['POST'])
@validate()
def user_register(body: RegisterUser) -> tp.Tuple[Response, int]:
    """
    Register user
    """

    data, status_code = validate_register_account_data(data=body)
    if status_code == 200:
        create_new_account(data=data)  # type: ignore
        return jsonify({'ok': 'Account has been register'}), status_code
    else:
        return jsonify(data), status_code


@app.route('/token/', methods=['POST'])
@validate()
def get_tokens(body: AccessToken) -> tp.Tuple[Response, int]:
    """
    Get tokens
    """

    data, status_code = validate_access_token_data(data=body)
    if status_code == 200:
        data = create_tokens(data={'username': data.username, 'password': data.password})  # type: ignore
        return jsonify(data), 200
    else:
        return jsonify(data), status_code


@app.route('/token_refresh/', methods=['POST'])
@validate()
def get_access_token_from_refresh(body: RefreshToken) -> tp.Tuple[Response, int]:
    data, status_code = generate_access_token_from_refresh(refresh_token=body.refresh_token)
    return jsonify(data), status_code


@app.route('/check/', methods=['POST'])
@authenticate
def check() -> tp.Tuple[Response, int]:
    # TODO ask
    print(request.user.email)  # type: ignore
    return jsonify({}), 200
