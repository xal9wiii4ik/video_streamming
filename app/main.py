import typing as tp
import logging

from pydantic import ValidationError

import settings

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from utils.before_request import validate_body_for_update_create, authenticate

from models import db
from utils.data_process import CustomJSONEncoder

from utils.error_handlers import (
    validation_error_handler,
    limit_offset_error_handler,
    sort_error_handler,
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

    # set custom json encoder
    app.json_encoder = CustomJSONEncoder

    # TODO it can be update to automatic
    app.before_request(authenticate)
    app.before_request(validate_body_for_update_create)

    app.register_error_handler(ValidationError, validation_error_handler)
    app.register_error_handler(LimitOffsetError, limit_offset_error_handler)
    app.register_error_handler(SortException, sort_error_handler)
    app.register_error_handler(PermissionException, permission_exception_handler)
    app.register_error_handler(EmptyBodyException, empty_body_exception)
    app.register_error_handler(SerializerValidationError, serializer_validation_error)

    # TODO it can be update to automatic
    app.register_blueprint(auth_urls)
    app.register_blueprint(account_urls)
    app.register_blueprint(video_urls)

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    return app


def initialize_models() -> None:
    """
    Initialize models
    Args:
        db: current db state
    """

    logging.info('Starting initialization of models')
    migrate = Migrate()
    migrate.init_app(app, db)
    db.init_app(app)


app: Flask = register_flask_application(settings.DEVELOPMENT_CONFIGURATION)
initialize_models()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
