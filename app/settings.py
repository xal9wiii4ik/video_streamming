import os
import typing as tp

# FLASK SETTINGS
SECRET_KEY: tp.Optional[str] = os.environ.get('SECRET_KEY')
FLASK_APP: tp.Optional[str] = os.environ.get('FLASK_APP')
FLASK_ENV: tp.Optional[str] = os.environ.get('FLASK_ENV')

# DB SETTINGS
DATABASE: tp.Optional[str] = os.environ.get('DATABASE')
POSTGRES_HOST: tp.Optional[str] = os.environ.get('POSTGRES_HOST')
POSTGRES_USER: tp.Optional[str] = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD: tp.Optional[str] = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB: tp.Optional[str] = os.environ.get('POSTGRES_DB')
POSTGRES_PORT: tp.Optional[str] = os.environ.get('POSTGRES_PORT')

# TEST DB SETTINGS
TEST_POSTGRES_HOST: tp.Optional[str] = 'db-test'
TEST_POSTGRES_USER: tp.Optional[str] = 'test_user'
TEST_POSTGRES_PASSWORD: tp.Optional[str] = 'test_password'
TEST_POSTGRES_DB: tp.Optional[str] = 'test_db'
TEST_POSTGRES_PORT: tp.Optional[str] = '5432'

# JWT SETTINGS
ACCESS_TOKEN_EXPIRE_MINUTES: tp.Optional[int] = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))  # type: ignore
REFRESH_TOKEN_EXPIRE_MINUTES: tp.Optional[int] = int(os.environ.get('REFRESH_TOKEN_EXPIRE_MINUTES'))  # type: ignore
DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = 180
DEFAULT_REFRESH_TOKEN_EXPIRE_MINUTES = 360
TOKEN_TYPE: tp.Optional[str] = os.environ.get('TOKEN_TYPE')
TOKEN_ALGORITHM: tp.Optional[str] = os.environ.get('TOKEN_ALGORITHM')
ACCESS_TOKEN_JWT_SUBJECT: tp.Optional[str] = os.environ.get('ACCESS_TOKEN_JWT_SUBJECT')
REFRESH_TOKEN_JWT_SUBJECT: tp.Optional[str] = os.environ.get('REFRESH_TOKEN_JWT_SUBJECT')

# CONFIGS
DEVELOPMENT_CONFIGURATION = {
    'SECRET_KEY': f'{SECRET_KEY}',
    'SQLALCHEMY_DATABASE_URI': f'{DATABASE}://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
                               f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}',
    'SQLALCHEMY_TRACK_MODIFICATIONS': True
}
TESTING_CONFIGURATION = {
    'SECRET_KEY': f'{SECRET_KEY}',
    'SQLALCHEMY_DATABASE_URI': f'postgresql://{TEST_POSTGRES_USER}:{TEST_POSTGRES_PASSWORD}'
                               f'@{TEST_POSTGRES_HOST}:{POSTGRES_PORT}/{TEST_POSTGRES_DB}',
    'SQLALCHEMY_TRACK_MODIFICATIONS': True
}
