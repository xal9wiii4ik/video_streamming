import typing as tp

from account.serializers import AccountModelSerializer

from models import Account, db
from utils.serializers import serializer_data_type


def create_new_account(data: tp.Dict[str, tp.Union[str, bool, int]]) -> serializer_data_type:
    """
    Create new account
    Args:
        data: register data
    Return:
        dict with account data
    """

    new_account = Account(**data, is_staff=False)
    db.session.add(new_account)
    db.session.commit()
    db.session.refresh(new_account)

    account_serializer = AccountModelSerializer(**new_account.__dict__)
    account_return_data: serializer_data_type = account_serializer.validate_data_before_get()
    return account_return_data
