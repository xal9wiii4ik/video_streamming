import typing as tp

from flask import Response, jsonify
from flask_pydantic import validate

from account.schemas import RegisterUser
from account.services_views import validate_create_account_data, create_new_account
from main import app


@app.route('/register/', methods=['POST'])
@validate()
def user_register(body: RegisterUser) -> tp.Tuple[Response, int]:
    """
    Register user
    """

    data, status_code = validate_create_account_data(data=body)
    if status_code == 200:
        create_new_account(data=data)  # type: ignore
        return jsonify({'ok': 'ok'}), status_code
    else:
        return jsonify(data), status_code
