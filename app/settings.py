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
SQL_USER: str = os.environ.get('SQL_USER')  # type: ignore
SQL_PASSWORD: str = os.environ.get('SQL_PASSWORD')  # type: ignore
SQL_DB_NAME: str = os.environ.get('SQL_DB_NAME')  # type: ignore
SQL_PORT: str = os.environ.get('SQL_PORT')  # type: ignore
