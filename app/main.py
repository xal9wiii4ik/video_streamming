import typing as tp
import logging
import settings

from flask import Flask, jsonify, Response

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def register_flask_application() -> Flask:
    """
    Register flask application
    Returns:
        current flask app
    """

    logging.info('Starting register application')
    app: Flask = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=settings.SECRET_KEY,
        SQLALCHEMY_DATABASE_URI=f'postgresql://{settings.SQL_USER}:{settings.SQL_PASSWORD}'
                                f'@{settings.SQL_HOST}:{settings.SQL_PORT}/{settings.SQL_DB_NAME}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
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

    from account.models import db

    logging.info('Starting initialization of models')
    db.init_app(app)


app: Flask = register_flask_application()
db: SQLAlchemy = register_db(application=app)
models_initialization()
# db.init_app(app)


@app.route('/')
def index() -> tp.Tuple[Response, int]:
    return jsonify({'ok': 'Main page'}), 200


if __name__ == "__main__":
    from account import app

    app.run(host="0.0.0.0", debug=True)
