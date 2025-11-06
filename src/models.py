

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from src.extensions import db


class BaseModel(db.Model):
    __abstract__ = True

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

## Models ##
class Account(BaseModel, UserMixin):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    name = Column(String)

    def __repr__(self):
        return f"<Account(id={self.id}, name='{self.name}', email='{self.username}')>"


# Base.metadata.create_all(db)

# class Account(db.Model, UserMixin):
#     __tablename__ = "account"

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, nullable=False)
#     password = db.Column(db.String, nullable=False)
#     name = db.Column(db.String, nullable=False)

#     def __init__(self, username, password, name):
#         self.username = username
#         self.password = generate_password_hash(password)
#         self.name = name

#     def __repr__(self):
#         return '<Account %r>' % (self.username)



