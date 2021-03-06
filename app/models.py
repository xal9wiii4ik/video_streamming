import datetime

from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()


class Account(db.Model):
    """
    Model for table account
    """

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(length=100), unique=True, nullable=False)
    password = db.Column(db.String(length=500), nullable=False)
    email = db.Column(db.String(length=100), nullable=False)
    first_name = db.Column(db.String(length=100), nullable=False)
    last_name = db.Column(db.String(length=100), nullable=False)
    is_staff = db.Column(db.Boolean(), default=False)


class Video(db.Model):
    """
    Model for table video
    """

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String(length=50), nullable=False)
    description = db.Column(db.String(length=1020), nullable=False)
    bucket_path = db.Column(db.String(length=100), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship('Account', backref=db.backref('video', lazy=True, cascade="all, delete-orphan"))
    upload_time = db.Column(db.DateTime, default=datetime.datetime.now)
