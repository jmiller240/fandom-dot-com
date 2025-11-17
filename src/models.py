

from sqlalchemy import Column, String, Integer, ForeignKey, Table
from flask_login import UserMixin

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
    "account_team",
    db.metadata,
    Column("account_id", Integer, ForeignKey("fandom_site.account.id"), primary_key=True),
    Column("team_id", Integer, ForeignKey("fandom_site.team.id"), primary_key=True),
    schema='fandom_site',
)

## Models ##
class Account(BaseModel, UserMixin):
    __tablename__ = "account"
    __table_args__ = {'schema': 'fandom_site'}

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
    __table_args__ = {'schema': 'fandom_site'}

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
    __table_args__ = {'schema': 'fandom_site'}

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
    league_id = Column(Integer, ForeignKey("fandom_site.league.id"))

    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}', league='{self.league_id}', espn_id='{self.espn_team_id}')>"


