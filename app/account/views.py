import typing as tp

from flask import Response, jsonify, request, Blueprint
from flask_pydantic import validate

from account.permissions import account_permission
from account.schemas import RegisterUser, AccessToken, RefreshToken, AccountData
from account.serializers import account_serializer
from account.services_views import (
    create_new_account,
    create_tokens,
    generate_access_token_from_refresh,
    authenticate,
    get_user_from_pk,
    update_account,
    remove_account,
    get_account
)
from account.validate_datas import validate_register_account_data, validate_access_token_data
from for_delete import func_rud_mixin
from models import Account

auth_urls = Blueprint('auth', __name__, url_prefix='/auth')
account_urls = Blueprint('account', __name__, url_prefix='/api/account')


@auth_urls.route('/register/', methods=['POST'])
@validate()
def user_register(body: RegisterUser) -> tp.Tuple[Response, int]:
    """
    Register user
    """

    data, status_code = validate_register_account_data(data=body)
    if status_code == 200:
        data = create_new_account(data=data)  # type: ignore
        return jsonify(data), status_code
    else:
        return jsonify(data), status_code


@auth_urls.route('/token/', methods=['POST'])
@validate()
def get_tokens(body: AccessToken) -> tp.Tuple[Response, int]:
    """
    Get tokens
    """

    data, status_code = validate_access_token_data(data=body)
    if status_code == 200:
        return_data = create_tokens(data={'username': data.username, 'password': data.password})  # type: ignore
        return_data.update({'user_pk': data.user_pk})  # type: ignore
        return jsonify(return_data), 200
    else:
        return jsonify(data), status_code


@auth_urls.route('/token_refresh/', methods=['POST'])
@validate()
def update_access_token(body: RefreshToken) -> tp.Tuple[Response, int]:
    """
    Update access token
    """

    data, status_code = generate_access_token_from_refresh(refresh_token=body.refresh_token)
    return jsonify(data), status_code


@account_urls.route('/<int:pk>/', methods=['GET', 'PATCH', 'DELETE'])
@authenticate
def user_detail(pk: int) -> tp.Tuple[Response, int]:
    """
    Get user
    """

    return func_rud_mixin(schema=AccountData,
                          model=Account,
                          request=request,
                          pk=pk,
                          serializer=account_serializer)
    # user_data, status_code = get_user_from_pk(pk=pk)
    # if status_code == 404:
    #     return jsonify(user_data), status_code
    #
    # has_permission = account_permission(user=request.user, request=request, pk=pk)  # type: ignore
    #
    # if not has_permission:
    #     return jsonify({'Error': 'You has not permissions to perform this action'}), 401
    #
    # if request.method == 'PATCH':
    #     data = AccountData(**request.json).__dict__  # type: ignore
    #     for key in data.copy().keys():
    #         if data[key] == '':
    #             del data[key]
    #     update_account(pk=pk, data=data)
    # elif request.method == 'DELETE':
    #     remove_account(pk=pk)
    #     return jsonify({}), 204
    # elif request.method == 'GET':
    #     return jsonify(user_data), status_code
    #
    # user_data, status_code = get_user_from_pk(pk=pk)
    # return jsonify(user_data), status_code


@account_urls.route('/', methods=['GET'])
@authenticate
def get_users() -> tp.Tuple[Response, int]:
    accounts, status_code = get_account()
    return jsonify(accounts), status_code
