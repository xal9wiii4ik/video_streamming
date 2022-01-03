import typing as tp

# from account.models import Account
# from main import db
from account.schemas import RegisterUser
from utils import make_password


def validate_create_account_data(data: RegisterUser) -> tp.Tuple[tp.Union[RegisterUser, tp.Dict[str, str]], int]:
    from account.models import Account
    # from main import db
    if data.password == data.repeat_password:
        password = make_password(data.password)
        data.password = password
        print(Account.query.filter_by(username=data.username).all())
        return data, 200
    else:
        # TODO check how get with keyword
        # print(Account.query.filter())
        # TODO add raise exception or return error code
        return {'ValidationError': 'password should be equal to repeat_password'}, 400


def create_new_account(data: RegisterUser) -> None:
    from main import db
    from account.models import Account

    new_post = Account(username=data.username,
                       password=data.password,
                       is_staff=False,
                       email=data.email,
                       first_name=data.first_name,
                       last_name=data.last_name)
    db.session.add(new_post)
    db.session.commit()
