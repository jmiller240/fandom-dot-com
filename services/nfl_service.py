import requests
from datetime import datetime
import pytz
import pprint
import pandas as pd



def format_date_from_date(s: str):
    dt = datetime.fromisoformat(s)
    
    if dt.year != datetime.today().year:
        date = datetime.strftime(dt, '%b %-d, %Y')
    else:
        date = datetime.strftime(dt, '%a, %b %-d')

    
    return date

def format_time_from_date(s: str):
    dt = datetime.fromisoformat(s)
    
    # 2. Define the target timezone (Central Time)
    central_timezone = pytz.timezone('America/Chicago')

    # 3. Convert the datetime object to the target timezone
    central_datetime = dt.astimezone(central_timezone)
    
    time = central_datetime.strftime("%-I:%M %p")
    return time

NFL_LEAGUE_OBJ = {
    'name': 'NFL',
    'logo-url': 'https://a.espncdn.com/i/teamlogos/leagues/500/nfl.png'
}

class NFLService:

    def __init__(self, teams_df):
        self.teams_df: pd.DataFrame = teams_df
        

    def get_team_schedule(self, team_id: int, season: int):
        print(f'preseason games')

        games = []
        for seasontype in [1,2,3]:
            # Url
            events_url = f'http://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{team_id}/schedule?season={season}&seasontype={seasontype}'
            
            response = requests.get(events_url)
            events = response.json()['events']
            print('Games: ', len(events))
            
            for game in events:
                event_id = game['id']

                date = format_date_from_date(game['date'])
                time = format_time_from_date(game['date'])
                season_obj = {
                    'name': game['season']['displayName'],
                    'type': game['seasonType']['name']
                }

                competition = game['competitions'][0]

                completed = competition['status']['type']['completed']
                print(completed)
                home_team = competition['competitors'][0]
                away_team = competition['competitors'][1]
                
                # Get home team logo
                home_team_id = int(home_team['id'])    
                away_team_id = int(away_team['id'])
                selected_team_is_home = team_id == home_team_id

                # if home_team_id not in self.teams_df['id'].tolist() or away_team_id not in self.teams_df['id'].tolist():
                #     continue

                home_team_logo = home_team['team']['logos'][0]['href']
                away_team_logo = away_team['team']['logos'][0]['href']

                result = None
                home_team_score = None
                away_team_score = None
                game_score_string = None
                selected_team_result = None
                if completed:
                    result = 'home' if home_team['winner'] else 'away' if away_team['winner'] else 'tie'
                    selected_team_result = 'tie' if result == 'tie' else 'win' if ((result == 'home' and selected_team_is_home) or (result == 'away' and not selected_team_is_home)) else 'loss'
                    home_team_score = int(home_team['score']['value'])
                    away_team_score = int(away_team['score']['value'])
                    game_score_string = str(away_team_score) + " - " + str(home_team_score)

                game_dict = {
                    'event_id': event_id,
                    'date': date,
                    'time': time,
                    'league': NFL_LEAGUE_OBJ,
                    'season': season_obj,
                    'completed': completed,
                    'home-team': home_team['team']['abbreviation'],
                    'home-team-logo': home_team_logo,
                    'home-team-score': home_team_score,
                    'away-team': away_team['team']['abbreviation'],
                    'away-team-logo': away_team_logo,
                    'away-team-score': away_team_score,
                    'game-score-string': game_score_string,
                    'winner': result,
                    'selected-team-result': selected_team_result
                }
                games.append(game_dict)

        return games

nfl_teams = pd.read_csv('../data/nfl_team_info.csv')
nba_teams = pd.read_csv('../data/nba_team_info.csv')
TEAMS_DF = pd.concat([nfl_teams, nba_teams]).reset_index(drop=True)
TEAMS_DF['app-id'] = TEAMS_DF.index

service = NFLService(teams_df=TEAMS_DF)
games = service.get_team_schedule(11, 2026)

pprint.pprint(games)