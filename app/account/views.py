from flask import Response, jsonify
from flask_pydantic import validate

from account.schemas import RegisterUser
from main import app


@app.route('/register/', methods=['POST'])
@validate()
def user_register(body: RegisterUser) -> Response:
    """
    Register user
    """

    print(body)
    return jsonify({'info': 'name'})
