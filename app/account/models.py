from main import db as model


class Account(model.Model):
    """
    Model for table account
    """

    id = model.Column(model.Integer(), primary_key=True, autoincrement=True)
    username = model.Column(model.String(length=100), unique=True)
    password = model.Column(model.String(length=500))
    email = model.Column(model.String(length=100))
    first_name = model.Column(model.String(length=100))
    last_name = model.Column(model.String(length=100))
    is_staff = model.Column(model.BOOLEAN())
