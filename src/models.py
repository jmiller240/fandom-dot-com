

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
    Column("team_id", Integer, ForeignKey("team.id"), primary_key=True),
)

## Models ##
class Account(BaseModel, UserMixin):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    name = Column(String)

    # relationships
    teams = db.relationship('Team', secondary=account_team_m2m, backref='account', lazy=True)

    def __repr__(self):
        return f"<Account(id={self.id}, name='{self.name}', email='{self.username}')>"


class League(BaseModel):
    __tablename__ = "league"

    id = Column(Integer, primary_key=True)
    espn_league_id = Column(Integer)
    name = Column(String)
    logo_url = Column(String)
    current_season = Column(String)
    current_season_type = Column(String)

    # relationships
    teams = db.relationship('Team', backref='league', lazy=True)

    def __repr__(self):
        return f"<League(id={self.id}, name='{self.name}', season='{self.current_season}')>"


class Team(BaseModel):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True)
    espn_team_id = Column(Integer)
    display_name = Column(String)
    location = Column(String)
    name = Column(String)
    short_display_name = Column(String)
    abbreviation = Column(String)
    color = Column(String)
    alternate_color = Column(String)
    logo_url = Column(String)
    league_id = Column(Integer, ForeignKey("league.id"))

    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}', league='{self.league_id}', espn_id='{self.espn_team_id}')>"


