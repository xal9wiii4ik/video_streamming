from main import db


class Account(db.Model):
    """
    Model for table account
    """

    __tablename__ = 'account'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(length=100), unique=True)
    email = db.Column(db.String(length=100))
    first_name = db.Column(db.String(length=100))
    last_name = db.Column(db.String(length=100))
