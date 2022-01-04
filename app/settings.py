import os

from pathlib import Path

from dotenv import load_dotenv

env_path = Path('.env')
load_dotenv(dotenv_path=env_path)

# FLASK SETTINGS
SECRET_KEY: str = os.environ.get('SECRET_KEY')  # type: ignore
FLASK_APP: str = os.environ.get('FLASK_APP')  # type: ignore
FLASK_ENV: str = os.environ.get('FLASK_ENV')  # type: ignore

# DB SETTINGS
SQL_HOST: str = os.environ.get('SQL_HOST')  # type: ignore
SQL_USER: str = os.environ.get('POSTGRES_USER')  # type: ignore
SQL_PASSWORD: str = os.environ.get('POSTGRES_PASSWORD')  # type: ignore
SQL_DB_NAME: str = os.environ.get('POSTGRES_DB')  # type: ignore
SQL_PORT: str = os.environ.get('SQL_PORT')  # type: ignore

# JWT SETTINGS
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))  # type: ignore
REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get('REFRESH_TOKEN_EXPIRE_MINUTES'))  # type: ignore
DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = 180
DEFAULT_REFRESH_TOKEN_EXPIRE_MINUTES = 360
TOKEN_TYPE: str = os.environ.get('TOKEN_TYPE')  # type: ignore
TOKEN_ALGORITHM: str = os.environ.get('TOKEN_ALGORITHM')  # type: ignore
ACCESS_TOKEN_JWT_SUBJECT: str = os.environ.get('ACCESS_TOKEN_JWT_SUBJECT')  # type: ignore
REFRESH_TOKEN_JWT_SUBJECT: str = os.environ.get('REFRESH_TOKEN_JWT_SUBJECT')  # type: ignore
