import typing as tp
import logging

from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

import settings

from flask import Flask, jsonify, Response
from flask_cors import CORS
from flask_migrate import Migrate

from utils.before_request import validate_body_for_update_create, authenticate

from models import db

from utils.error_handlers import (
    validation_error_handler,
    limit_offset_error_handler,
    sort_error_handler,
    integrity_error_handler,
    permission_exception_handler,
    empty_body_exception,
    serializer_validation_error,
)
from utils.exceptions import (
    LimitOffsetError,
    SortException,
    PermissionException,
    EmptyBodyException,
    SerializerValidationError,
)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def register_flask_application(config: tp.Any) -> Flask:
    """
    Register flask application
    Returns:
        current flask app
    """

    from auth.views import auth_urls
    from account.views import account_urls
    from video.views import video_urls

    logging.info('Starting register application')
    app: Flask = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(**config)

    # TODO it can be update to automatic
    app.before_request(authenticate)
    app.before_request(validate_body_for_update_create)

    app.register_error_handler(ValidationError, validation_error_handler)
    app.register_error_handler(LimitOffsetError, limit_offset_error_handler)
    app.register_error_handler(SortException, sort_error_handler)
    app.register_error_handler(IntegrityError, integrity_error_handler)
    app.register_error_handler(PermissionException, permission_exception_handler)
    app.register_error_handler(EmptyBodyException, empty_body_exception)
    app.register_error_handler(SerializerValidationError, serializer_validation_error)

    # TODO it can be update to automatic
    app.register_blueprint(auth_urls)
    app.register_blueprint(account_urls)
    app.register_blueprint(video_urls)

    @app.route('/', methods=["GET", "POST"])
    def index() -> tp.Tuple[Response, int]:
        return jsonify({'ok': 'Main page'}), 200

    CORS(app)

    return app


def models_initialization() -> None:
    """
    Initialize models
    Args:
        db: current db state
    """

    logging.info('Starting initialization of models')
    Migrate(app, db, directory='migrations')
    db.init_app(app)


app: Flask = register_flask_application(settings.DEVELOPMENT_CONFIGURATION)
models_initialization()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
