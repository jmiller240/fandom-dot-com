

from src import db
from src.models import League, Team


class DatabaseService:

    def __init__(self):
        super().__init__()

    def get_leagues(self) -> list[League]:
        # Get leagues
        leagues = League.query.all()
        return leagues
    
    def get_teams(self) -> list[Team]:
        # Get leagues and teams
        all_teams = Team.query.all()
        return all_teams

    def get_team(self, id: int) -> Team:
        # Get info from DB
        t: Team = Team.query.filter_by(id=id).first()
        return t
    
    def get_league(self, id: int) -> League:
        l: League = League.query.filter_by(id=id).first()
        return l