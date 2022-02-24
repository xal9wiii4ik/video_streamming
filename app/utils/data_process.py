import hashlib
import typing as tp
from typing import Iterable

from flask.json import JSONEncoder

from datetime import date

from settings import SECRET_KEY

type_model_data = tp.Tuple[tp.Union[tp.List[tp.Dict[str, tp.Union[str, bool]]], tp.Dict[str, tp.Union[str, bool]]], int]


MAGIC_NUMBER = 100000


def make_password(password: str) -> str:
    """
    Hashing password
    Args:
         password: password
    Returns:
        hex of hashing password
    """

    hash_password = hashlib.pbkdf2_hmac('sha256',
                                        password.encode('utf-8'),
                                        SECRET_KEY.encode('utf-8'),  # type: ignore
                                        MAGIC_NUMBER)
    return hash_password.hex()


class CustomJSONEncoder(JSONEncoder):
    """
    Custom json encoder
    """

    def default(self, obj: tp.Any) -> tp.Any:
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, Iterable):
            return list(iter(obj))
        return JSONEncoder.default(self, obj)
