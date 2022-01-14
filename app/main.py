import typing as tp
import logging
import settings

from flask import Flask, jsonify, Response

from flask_cors import CORS
from flask_migrate import Migrate

from models import db

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def register_flask_application(config: tp.Any) -> Flask:
    """
    Register flask application
    Returns:
        current flask app
    """

    from account.views import auth_urls, account_urls
    from video.views import video_urls

    logging.info('Starting register application')
    app: Flask = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(**config)

    app.register_blueprint(auth_urls)
    app.register_blueprint(account_urls)
    app.register_blueprint(video_urls)

    @app.route('/')
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
