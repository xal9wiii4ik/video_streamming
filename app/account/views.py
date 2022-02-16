import typing as tp

from flask import request, Blueprint, jsonify, Response
from flask.views import MethodView

from account.serializers import RegisterUserSerializer, AccountModelSerializer
from account.services_views import create_new_account

from models import Account

from utils.mixins import ListCreateViewMixin

account_urls = Blueprint('account', __name__, url_prefix='/api/account')


class RegisterAccountView(MethodView):
    """ Register new user """

    methods = ['POST']

    def post(self) -> tp.Tuple[Response, int]:
        serializer = RegisterUserSerializer(**request.json)  # type: ignore
        serializer.update_remove_fields(fields=['repeat_password'])
        serializer_data = serializer.validate_data_before_create()
        model_data = create_new_account(data=serializer_data)
        return jsonify(model_data), 200


class AccountListView(ListCreateViewMixin):
    """
    View for getting all accounts
    """

    methods = ['GET']
    model = Account
    request = request
    serializer = AccountModelSerializer


account_urls.add_url_rule('/register/', view_func=RegisterAccountView.as_view('register'))
account_urls.add_url_rule('/', view_func=AccountListView.as_view('account-list'))
