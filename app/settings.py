import os

# FLASK SETTINGS
SECRET_KEY: str = os.environ.get('SECRET_KEY')  # type: ignore
FLASK_APP: str = os.environ.get('FLASK_APP')  # type: ignore
FLASK_ENV: str = os.environ.get('FLASK_ENV')  # type: ignore

# DB SETTINGS
POSTGRES_HOST: str = os.environ.get('POSTGRES_HOST')  # type: ignore
POSTGRES_USER: str = os.environ.get('POSTGRES_USER')  # type: ignore
POSTGRES_PASSWORD: str = os.environ.get('POSTGRES_PASSWORD')  # type: ignore
POSTGRES_DB: str = os.environ.get('POSTGRES_DB')  # type: ignore
POSTGRES_PORT: str = os.environ.get('POSTGRES_PORT')  # type: ignore

# TEST DB SETTINGS
TEST_POSTGRES_HOST: str = 'db-test'
TEST_POSTGRES_USER: str = 'test_user'
TEST_POSTGRES_PASSWORD: str = 'test_password'
TEST_POSTGRES_DB: str = 'test_db'
TEST_POSTGRES_PORT: str = '5432'

# JWT SETTINGS
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))  # type: ignore
REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get('REFRESH_TOKEN_EXPIRE_MINUTES'))  # type: ignore
DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = 180
DEFAULT_REFRESH_TOKEN_EXPIRE_MINUTES = 360
TOKEN_TYPE: str = os.environ.get('TOKEN_TYPE')  # type: ignore
TOKEN_ALGORITHM: str = os.environ.get('TOKEN_ALGORITHM')  # type: ignore
ACCESS_TOKEN_JWT_SUBJECT: str = os.environ.get('ACCESS_TOKEN_JWT_SUBJECT')  # type: ignore
REFRESH_TOKEN_JWT_SUBJECT: str = os.environ.get('REFRESH_TOKEN_JWT_SUBJECT')  # type: ignore

# CONFIGS
DEVELOPMENT_CONFIGURATION = {
    'SECRET_KEY': f'{SECRET_KEY}',
    'SQLALCHEMY_DATABASE_URI': f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
                               f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}',
    'SQLALCHEMY_TRACK_MODIFICATIONS': True
}
TESTING_CONFIGURATION = {
    'SECRET_KEY': f'{SECRET_KEY}',
    'SQLALCHEMY_DATABASE_URI': f'postgresql://{TEST_POSTGRES_USER}:{TEST_POSTGRES_PASSWORD}'
                               f'@{TEST_POSTGRES_HOST}:{POSTGRES_PORT}/{TEST_POSTGRES_DB}',
    'SQLALCHEMY_TRACK_MODIFICATIONS': True
}
