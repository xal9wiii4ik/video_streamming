from main import db as model


class Account(model.Model):
    """
    Model for table account
    """

    __tablename__ = 'account'

    id = model.Column(model.Integer(), primary_key=True, autoincrement=True)
    username = model.Column(model.String(length=100), unique=True)
    password = model.Column(model.String(length=500))
    email = model.Column(model.String(length=100))
    first_name = model.Column(model.String(length=100))
    last_name = model.Column(model.String(length=100))
    is_staff = model.Column(model.BOOLEAN())

    def __init__(self, username: str,
                 password: str,
                 email: str,
                 first_name: str,
                 last_name: str,
                 is_staff: bool = False) -> None:
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_staff = is_staff
