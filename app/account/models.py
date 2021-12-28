from main import db


class Account(db.Model):
    """
    Model for table account
    """

    __tablename__ = 'account'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(length=100), unique=True)
    password = db.Column(db.String(length=500))
    email = db.Column(db.String(length=100))
    first_name = db.Column(db.String(length=100))
    last_name = db.Column(db.String(length=100))
    is_staff = db.Column(db.BOOLEAN())

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
