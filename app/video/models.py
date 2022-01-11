from main import db as models


class Video(models.Model):
    """
    Model for table video
    """

    __tablename__ = 'video'

    id = models.Column(models.Integer(), primary_key=True, autoincrement=True)
    title = models.Column(models.String(length=50))
    description = models.Column(models.String(length=1020))
    bucket_path = models.Column(models.String(length=100))
    account_id = models.Column(models.Integer, models.ForeignKey('account.id'), nullable=False)
    account = models.relationship('Account', backref=models.backref('video', lazy=True))
