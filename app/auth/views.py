import typing as tp
import settings

from flask import Response, jsonify, Blueprint, request
from flask.views import MethodView

from auth.serializers import AccessTokenSerializer, RefreshTokenSerializer
from auth.services_views import (
    create_tokens,
    generate_access_token_from_refresh,
)

auth_urls = Blueprint('auth', __name__, url_prefix='/auth')


class GetTokensView(MethodView):
    """
    Get tokens
    """

    methods = ['POST']

    def post(self) -> tp.Tuple[Response, int]:
        serializer = AccessTokenSerializer(**request.json)  # type: ignore
        serializer_data = serializer.validate_data_before_create()
        tokens_data = create_tokens(data=serializer_data)
        tokens_data.update({'access_token_expire': settings.ACCESS_TOKEN_EXPIRE_MINUTES})  # type: ignore
        tokens_data.update({'user_pk': serializer.user_pk})  # type: ignore
        return jsonify(tokens_data), 200


class RefreshTokenView(MethodView):
    """
    Update access token using refresh token
    """

    methods = ['POST']

    def post(self) -> tp.Tuple[Response, int]:
        serializer = RefreshTokenSerializer(**request.json)  # type: ignore
        serializer_data = serializer.validate_data_before_create()
        tokens_data = generate_access_token_from_refresh(
            refresh_token=serializer_data.get('refresh_token')  # type: ignore
        )
        tokens_data.update({'access_token_expire': settings.ACCESS_TOKEN_EXPIRE_MINUTES})  # type: ignore
        return jsonify(tokens_data), 200


auth_urls.add_url_rule('/token/', view_func=GetTokensView.as_view('token'))
auth_urls.add_url_rule('/token_refresh/', view_func=RefreshTokenView.as_view('token_refresh'))
