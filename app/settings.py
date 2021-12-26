import os
import typing as tp

from pathlib import Path

from dotenv import load_dotenv

env_path = Path('.env')
load_dotenv(dotenv_path=env_path)

# FLASK SETTINGS
SECRET_KEY: tp.Optional[str] = os.environ.get('SECRET_KEY')
FLASK_APP: tp.Optional[str] = os.environ.get('FLASK_APP')
FLASK_ENV: tp.Optional[str] = os.environ.get('FLASK_ENV')

# DB SETTINGS
SQL_HOST: tp.Optional[str] = os.environ.get('SQL_HOST')
SQL_USER: tp.Optional[str] = os.environ.get('SQL_USER')
SQL_PASSWORD: tp.Optional[str] = os.environ.get('SQL_PASSWORD')
SQL_DB_NAME: tp.Optional[str] = os.environ.get('SQL_DB_NAME')
SQL_PORT: tp.Optional[str] = os.environ.get('SQL_PORT')
