import typing as tp

from flask import Response, request, Blueprint

from utils.permissions import is_owner
from account.schemas import AccountData
from auth.services_views import authenticate

from utils.data_process import validate_data_for_create_or_update
from utils.endpoint_mixins import detail_endpoint_mixin, list_endpoint_mixin

from models import Account

account_urls = Blueprint('account', __name__, url_prefix='/api/account')


@account_urls.route('/<int:pk>/', methods=['GET', 'PATCH', 'DELETE'])
@authenticate
def user_detail(pk: int) -> tp.Tuple[Response, int]:
    """
    Detail user
    """

    data = validate_data_for_create_or_update(schema=AccountData, request=request)
    return detail_endpoint_mixin(schema=AccountData,
                                 model=Account,
                                 request=request,
                                 pk=pk,
                                 data=data,
                                 permissions=[is_owner])


@account_urls.route('/', methods=['GET'])
@authenticate
def list_users() -> tp.Tuple[Response, int]:
    """
    List user
    """

    return list_endpoint_mixin(schema=AccountData, model=Account, request=request)
