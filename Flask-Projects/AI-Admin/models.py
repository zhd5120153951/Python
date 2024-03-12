from extensions import db
from datetime import datetime
import sqlalchemy as sa


class Student(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(length=20))
    username = sa.Column(sa.String(length=20))
    mail = sa.Column(sa.String(length=50))
    sex = sa.Column(sa.String(length=1))
    birthdate = sa.Column(sa.DATE, default=datetime.now)
    address = sa.Column(sa.Text)


class User(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(length=20))
    username = sa.Column(sa.String(length=20))
    password = sa.Column(sa.String(length=20))
    address = sa.Column(sa.String(length=20))
