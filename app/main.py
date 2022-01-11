import typing as tp
import logging
import settings

from flask import Flask, jsonify, Response

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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


def register_db(application: Flask) -> SQLAlchemy:
    """
    Register db for appliciation
    Returns:
        current db session
    """

    db: SQLAlchemy = SQLAlchemy()
    Migrate(application, db, directory='migrations')
    return db


def models_initialization() -> None:
    """
    Initialize models
    Args:
        db: current db state
    """

    # from account.models import Account

    logging.info('Starting initialization of models')
    app.app_context().push()
    db.init_app(app)
    db.create_all()


app: Flask = register_flask_application(settings.DEVELOPMENT_CONFIGURATION)
db: SQLAlchemy = register_db(application=app)
models_initialization()

if __name__ == "__main__":
    from account.models import Account
    from video.models import Video
    app.run(host="0.0.0.0", debug=True)
