import requests
from datetime import datetime
import pytz
import pprint
import pandas as pd

from ..helpers.functions import format_datetime_from_date, format_date_from_date, format_time_from_date


NFL_LEAGUE_OBJ = {
    'name': 'NFL',
    'logo-url': 'https://a.espncdn.com/i/teamlogos/leagues/500/nfl.png'
}
NBA_LEAGUE_OBJ = {
    'name': 'NBA',
    'logo-url': 'https://a.espncdn.com/i/teamlogos/leagues/500/nba.png'
}

# http://site.api.espn.com/apis/site/v2/sports/football/nfl/seasons/2025/teams/11




class ESPNAPIService:

    def __init__(self, teams_df: pd.DataFrame):
        self.teams_df: pd.DataFrame = teams_df
    
    def _get_site_api_espn_base_url(self, league):
        if league == 'NFL':
            return 'http://site.api.espn.com/apis/site/v2/sports/football/nfl'
        elif league == 'NBA':
            return 'http://site.api.espn.com/apis/site/v2/sports/basketball/nba'
        elif league == 'CFB':
            return 'http://site.api.espn.com/apis/site/v2/sports/football/college-football'
        elif league == 'MLB':
            return 'http://site.api.espn.com/apis/site/v2/sports/baseball/mlb'
        elif league == 'PREM':
            return 'http://site.api.espn.com/apis/site/v2/sports/soccer/eng.1'

    def _get_sports_core_api_espn_base_url(self, league):
        if league == 'NFL':
            return 'https://sports.core.api.espn.com/v2/sports/football/leagues/nfl'
        elif league == 'NBA':
            return 'https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba'
        elif league == 'CFB':
            return 'https://sports.core.api.espn.com/v2/sports/football/leagues/college-football'
        elif league == 'MLB':
            return 'https://sports.core.api.espn.com/v2/sports/baseball/leagues/mlb'
        elif league == 'PREM':
            return 'https://sports.core.api.espn.com/v2/sports/soccer/leagues/eng.1'

    def get_partners_api_espn_base_url(self, league: str):
        if league == 'NFL':
            return 'https://partners.api.espn.com/v2/sports/football/nfl'
        elif league == 'NBA':
            return 'https://partners.api.espn.com/v2/sports/basketball/nba'
        elif league == 'CFB':
            return 'https://partners.api.espn.com/v2/sports/football/college-football'
        elif league == 'MLB':
            return 'https://partners.api.espn.com/v2/sports/baseball/mlb'
        elif league == 'PREM':
            return 'https://partners.api.espn.com/v2/sports/soccer/eng.1'

    def get_league_current_season(self, league: str) -> int:
        base_url = self._get_sports_core_api_espn_base_url(league=league)
        response = requests.get(base_url).json()

        return int(response['season']['year'])

    def get_league_info(self, league: str):
        base_url = self._get_sports_core_api_espn_base_url(league=league)
        response = requests.get(base_url).json()

        league_info = {
            'id': response['id'],
            'name': league,
            'logo-url': response['logos'][0]['href'],
            'current-season': response['season']['year'],
            'current-season-type': response['season']['type']['type']
        }
        return league_info

    def get_team_info(self, league: str, team_id: int, season: int):
        # Hit API
        base_url = self._get_site_api_espn_base_url(league=league)
        info_url = f'{base_url}/teams/{team_id}'
        response = requests.get(info_url).json()

        # Put it all together
        team_obj = {
            'id': team_id,
            'name': response['team']['name'],
            'full-name': response['team']['displayName'],
            'logo-url': response['team']['logos'][0]['href']
        }

        # Get league info
        league_obj = self.get_league_info(league=league)
        team_obj['league'] = league_obj

        # Get record
        base_url = self.get_partners_api_espn_base_url(league=league)
        info_url = f'{base_url}/teams/{team_id}?season={season}'
        response = requests.get(info_url).json()

        record_obj = {}
        for record in response['team']['record']:
            record_name = record['name']
            record_value = record['displayValue']

            record_obj[record_name] = record_value

        team_obj['record'] = record_obj


        return team_obj


    def get_team_schedule(self, league: str, team_id: int, season: int):
        print(f'preseason games')

        # League
        league_obj = self.get_league_info(league=league)

        games = []
        for seasontype in [1,2,3]:
            # Url
            base_url = self._get_site_api_espn_base_url(league=league)
            events_url = f'{base_url}/teams/{team_id}/schedule?season={season}&seasontype={seasontype}'
            
            response = requests.get(events_url)
            events = response.json()['events']
            print('Games: ', len(events))
            
            for game in events:
                event_id = game['id']
                competition = game['competitions'][0]

                # Game info
                dt = format_datetime_from_date(game['date'])
                date = format_date_from_date(game['date'])
                time = format_time_from_date(game['date'])
                season_obj = {
                    'name': game['season']['displayName'],
                    'type': game['seasonType']['name']
                }
                headline = competition['notes'][0]['headline'] if competition['notes'] else ''

                completed = competition['status']['type']['completed']
                home_team = competition['competitors'][0]
                away_team = competition['competitors'][1]
                
                # Get home team logo
                selected_team_is_home = (team_id == int(home_team['id']))  

                home_team_logo = home_team['team']['logos'][0]['href']
                away_team_logo = away_team['team']['logos'][0]['href']

                result = None
                home_team_score = None
                away_team_score = None
                game_score_string = None
                selected_team_result = None

                # name = STATUS_IN_PROGRESS
                if completed:
                    result = 'home' if home_team['winner'] else 'away' if away_team['winner'] else 'tie'
                    selected_team_result = 'tie' if result == 'tie' else 'win' if ((result == 'home' and selected_team_is_home) or (result == 'away' and not selected_team_is_home)) else 'loss'
                    home_team_score = int(home_team['score']['value'])
                    away_team_score = int(away_team['score']['value'])
                    game_score_string = str(away_team_score) + " - " + str(home_team_score)

                game_dict = {
                    'event_id': event_id,
                    'datetime': dt,
                    'date': date,
                    'time': time,
                    'league': league_obj,
                    'season': season_obj,
                    'headline': headline,
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
    
    def get_game_info(self, league: str, event_id: int):
        ## Hit API
        base_url = self._get_site_api_espn_base_url(league=league)
        event_url = f'{base_url}/summary?event={event_id}'
        response = requests.get(event_url).json()

        ## General game info
        
        # Get league info
        league_obj = self.get_league_info(league=league)

        # Season
        season_obj = {
            'year': response['header']['season']['year'],
            'type': response['header']['season']['type']
        }

        competition = response['header']['competitions'][0]

        game_status = competition['status']['type']['name']
        game_completed = competition['status']['type']['completed']

        date = format_date_from_date(competition['date'])
        start_time = format_time_from_date(competition['date'])
        venue = response['gameInfo']['venue']['fullName']
        city = response['gameInfo']['venue']['address']['city']
        state = response['gameInfo']['venue']['address']['state']
        
        attendance = response['gameInfo']['attendance'] if game_completed else 0
        game_winner = None

        ## Home team info
        home_team_obj = competition['competitors'][0]
        home_team_id = int(home_team_obj['team']['id'])
        home_team = {
            'id': home_team_id,
            'name': home_team_obj['team']['name'],
            'logo_url': home_team_obj['team']['logos'][0]['href'],
            'winner': False,
        }

        ## Away team info
        away_team_obj = competition['competitors'][1]
        away_team_id = int(away_team_obj['team']['id'])
        away_team = {
            'id': away_team_id,
            'name': away_team_obj['team']['name'],
            'logo_url': away_team_obj['team']['logos'][0]['href'],
            'winner': False,
        }

        if game_completed:
            ## Home team scores
            home_team['winner'] = home_team_obj['winner'],

            home_team_score_obj = home_team_obj['linescores']
            periods_in_game = len(home_team_score_obj)

            # Regulation line scores
            home_team['score'] = {f'Q{i + 1}': home_team_score_obj[i]['displayValue'] for i in range(0, 4)}
            
            # Add in OT
            if periods_in_game > 4:
                if periods_in_game == 5:
                    home_team['score']['OT'] = home_team_score_obj[4]['displayValue']
                else:
                    ot_period = 1
                    for i in range(4, periods_in_game):
                        home_team['score'][f'OT{ot_period}'] = home_team_score_obj[i]['displayValue']
                        ot_period += 1
            
            # Total score
            home_team['score']['Total'] = home_team_obj['score']
            
            ## Away team scores
            away_team['winner'] = away_team_obj['winner'],

            away_team_score_obj = away_team_obj['linescores']
            periods_in_game = len(away_team_score_obj)

            # Regulation line scores
            away_team['score'] = {f'Q{i + 1}': away_team_score_obj[i]['displayValue'] for i in range(0, 4)}
            
            # Add in OT
            if periods_in_game > 4:
                if periods_in_game == 5:
                    away_team['score']['OT'] = away_team_score_obj[4]['displayValue']
                else:
                    ot_period = 1
                    for i in range(4, periods_in_game):
                        away_team['score'][f'OT{ot_period}'] = away_team_score_obj[i]['displayValue']
                        ot_period += 1
            
            # Total score
            away_team['score']['Total'] = away_team_obj['score']

            game_winner = 'home' if home_team['winner'] else 'away'

        ## Final game object
        game_info = {
            'date': date,
            'start-time': start_time,
            'venue': venue,
            'city': city,
            'state': state,
            'completed': game_completed,
            'attendance': attendance,
            'league': league_obj,
            'season': season_obj,
            'home-team': home_team,
            'away-team': away_team,
            'winner': game_winner
        }

        return game_info
