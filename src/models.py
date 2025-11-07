

from sqlalchemy import Column, String, Integer, ForeignKey, Table
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




# Define the association table (bridge table)
account_team_m2m = Table(
    "account_teams",
    db.metadata,
    Column("account_id", Integer, ForeignKey("account.id"), primary_key=True),
    Column("team_id", Integer, ForeignKey("team.appID"), primary_key=True),
)

## Models ##
class Account(BaseModel, UserMixin):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    name = Column(String)

    # relationships
    # teams = db.relationship('AccountTeams', lazy=True) # backref='author',
    teams = db.relationship('Team', secondary=account_team_m2m, backref='accounts', lazy=True)

    def __repr__(self):
        return f"<Account(id={self.id}, name='{self.name}', email='{self.username}')>"

# class AccountTeams(BaseModel):
#     __tablename__ = "account_teams"

#     id = Column(Integer, primary_key=True)
#     account_id = Column(Integer, ForeignKey('account.id'))
#     team_id = Column(Integer, ForeignKey('team.appID'))

#     def __repr__(self):
#         return f"<AccountTeam(user_id={self.account_id}, team='{self.team_id}')>"


class Team(BaseModel):
    __tablename__ = "team"

    id = Column(Integer)
    displayName = Column(String)
    location = Column(String)
    name = Column(String)
    shortDisplayName = Column(String)
    abbreviation = Column(String)
    color = Column(String)
    alternateColor = Column(String)
    logoURL = Column(String)
    league = Column(String)
    appID = Column(String, primary_key=True)

    # relationships
    # accounts = db.relationship('AccountTeams', lazy=True)
    
    def __repr__(self):
        return f"<Team(appID={self.appID}, name='{self.name}', name='{self.league}', name='{self.id}')>"



