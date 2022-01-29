import typing as tp


def create_new_account(data: tp.Dict[str, tp.Union[str, bool, int]]) -> tp.Dict[str, tp.Union[str, bool, int]]:
    """
    Create new account
    Args:
        data: register data
    Return:
        dict with account data
    """

    from main import db
    from models import Account

    data['is_staff'] = False

    new_account = Account(**data)
    db.session.add(new_account)
    db.session.commit()

    data['id'] = new_account.id
    del data['password']
    return data
