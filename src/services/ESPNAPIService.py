
from flask import session


import requests
from datetime import datetime, date
import pytz
import pprint
import pandas as pd

from ..helpers.functions import format_datetime_from_date, format_date_from_date, format_time_from_date
from ..helpers.constants import LEAGUES



class ESPNAPIService:

    def __init__(self):
        pass  
    
    ''' Public '''

    def get_games(self, date: date):

        # Variables
        date_str = date.strftime('%Y%m%d')

        # Get games for each league
        league_games = []
        for league in LEAGUES.keys():
            # Hit API for games
            url = self._get_scoreboard_url(league=league, date_str=date_str)
            response = self._api_call(url)

            # Process games
            league_season_name = response['leagues'][0]['season']['type']['name']
            events = response['events']

            if not events:
                continue
            
            games = []
            for event in events:
                game_dict = self._parse_event(event)
                game_dict['season']['name'] = league_season_name
                games.append(game_dict)
        
            # Make dict to return
            d = {
                'league': self.get_league_info(league),
                'games_list': games
            }
            league_games.append(d)
        
        return league_games

    def get_league_current_season(self, league: str) -> int:
        league_info = self.get_league_info(league=league)
        return int(league_info['current-season'])

    def get_league_info(self, league: str):
        if 'leagues' not in session:
            session['leagues'] = {}

        # Try to pull from cache
        if league in session['leagues']:
            return session['leagues'][league]
        
        else:
            # If not, pull from API and cache
            base_url = self._get_sports_core_api_espn_base_url(league=league)
            response = self._api_call(base_url)

            league_info = {
                'id': response['id'],
                'name': league,
                'display_name': response['name'],
                'logo_url': response['logos'][0]['href'],
                'current_season': response['season']['year'],
                'current_season_type': response['season']['type']['type']
            }

            # Cache object
            session['leagues'][league] = league_info
            
            return league_info

    def get_league_games(self, league: str, date: date):
        # Hit API
        date_str = date.strftime('%Y%m%d')
        url = self._get_scoreboard_url(league=league, date_str=date_str)
        response = self._api_call(url)

        # Process records
        league_season_name = response['leagues'][0]['season']['type']['name']
        events = response['events']
        games = []

        for event in events:
            game_dict = self._parse_event(event)
            game_dict['season']['name'] = league_season_name
            games.append(game_dict)
        
        return games

    def get_team_record(self, league: str, team_id: int, season: int):
        # Hit API
        base_url = self._get_partners_api_espn_base_url(league=league)
        info_url = f'{base_url}/teams/{team_id}?season={season}'
        response = self._api_call(info_url)

        # Process records
        record_obj = {}
        
        # if 'record' in response['team']: 
        for record in response['team']['record']:
            record_name = record['name']
            record_value = record['displayValue']

            record_obj[record_name] = record_value

        return record_obj
    
    def get_team_info(self, league: str, team_id: int, season: int):
        if 'teams' not in session:
            session['teams'] = {}
        
        s_team_id = str(team_id)
        if s_team_id in session['teams']:
            return session['teams'][s_team_id]

        else:
            # Hit API
            base_url = self._get_site_api_espn_base_url(league=league)
            info_url = f'{base_url}/teams/{team_id}'
            response = self._api_call(info_url)

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
            base_url = self._get_partners_api_espn_base_url(league=league)
            info_url = f'{base_url}/teams/{team_id}?season={season}'
            response = self._api_call(info_url)

            record_obj = {}
            for record in response['team']['record']:
                record_name = record['name']
                record_value = record['displayValue']

                record_obj[record_name] = record_value

            team_obj['record'] = record_obj

            # Cache object
            session['teams'][team_id] = team_obj

            return team_obj

    def get_team_schedule(self, league: str, team_id: int, season: int):

        games = []
        for seasontype in [1,2,3]:
            print('Season type:', seasontype)
            
            # Url
            base_url = self._get_site_api_espn_base_url(league=league)
            events_url = f'{base_url}/teams/{team_id}/schedule?season={season}&seasontype={seasontype}'
                   
            response = self._api_call(events_url)
            events = response['events']
            print('Games: ', len(events))
            
            for event in events:
                # Parse game
                game_dict = self._parse_event(event)

                # Get selected team result
                selected_team_result = None
                if game_dict['result'] == 'tie':
                    selected_team_result = 'tie'
                elif game_dict['result'] == 'home' and int(game_dict['home_team']['id']) == team_id:
                    selected_team_result = 'win'
                elif game_dict['result'] == 'away' and int(game_dict['away_team']['id']) == team_id:
                    selected_team_result = 'win'
                else:
                    selected_team_result = 'loss'
                game_dict['selected_team_result'] = selected_team_result

                games.append(game_dict)
        
        games = sorted(games, key=lambda game: game['datetime'])

        return games



    def get_team_schedule_OLD(self, league: str, team_id: int, season: int):

        # League
        league_obj = self.get_league_info(league=league)

        games = []
        for seasontype in [1,2,3]:
            print('Season type:', seasontype)
            
            # Url
            base_url = self._get_site_api_espn_base_url(league=league)
            events_url = f'{base_url}/teams/{team_id}/schedule?season={season}&seasontype={seasontype}'
            
            response = self._api_call(events_url)
            events = response['events']
            print('Games: ', len(events))
            
            for game in events:
                event_id = game['id']
                competition = game['competitions'][0]
                home_team = competition['competitors'][0]
                away_team = competition['competitors'][1]

                # Game info
                dt = format_datetime_from_date(game['date'])
                date = format_date_from_date(game['date'])
                time = format_time_from_date(game['date'])
                season_obj = {
                    'name': game['season']['displayName'],
                    'type': game['seasonType']['name']
                }
                headline = competition['notes'][0]['headline'] if competition['notes'] else ''

                status = competition['status']['type']['name']
                status_display = competition['status']['type']['shortDetail']
                completed = competition['status']['type']['completed']
                
                # Get home team logo
                selected_team_is_home = (team_id == int(home_team['id']))  

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
                elif status == 'STATUS_IN_PROGRESS':
                    # TODO - find an API with live score
                    home_team_score = int(home_team['score']['value']) if 'score' in home_team else ''
                    away_team_score = int(away_team['score']['value']) if 'score' in away_team else ''
                    game_score_string = str(away_team_score) + " - " + str(home_team_score)

                game_dict = {
                    'event_id': event_id,
                    'datetime': dt,
                    'date': date,
                    'time': time,
                    'league': league_obj,
                    'season': season_obj,
                    'headline': headline,
                    'status': status_display,
                    'in_progress': (status == 'STATUS_IN_PROGRESS'),
                    'completed': completed,
                    'home-team': home_team['team']['abbreviation'],
                    'home-team-logo': home_team_logo,
                    'home-team-score': home_team_score,
                    'away-team': away_team['team']['abbreviation'],
                    'away-team-logo': away_team_logo,
                    'away-team-score': away_team_score,
                    'game_score_string': game_score_string,
                    'winner': result,
                    'selected-team-result': selected_team_result
                }
                games.append(game_dict)

        return games
    
    def get_game_info(self, league: str, event_id: int):
        ## Hit API
        base_url = self._get_site_api_espn_base_url(league=league)
        event_url = f'{base_url}/summary?event={event_id}'
        response = self._api_call(event_url)

        ## General game info
        
        # Get league info
        league_obj = self.get_league_info(league=league)

        # Season
        season_obj = {
            'year': response['header']['season']['year'],
            'type': response['header']['season']['type']
        }

        # Objects
        game_info = response['gameInfo']
        competition = response['header']['competitions'][0]
        home_team_obj = competition['competitors'][0]
        away_team_obj = competition['competitors'][1]

        # Status
        status = competition['status']['type']['name']
        status_display = competition['status']['type']['shortDetail']
        in_progress = (status == 'STATUS_IN_PROGRESS')
        completed = competition['status']['type']['completed']

        # Competition info
        date = format_date_from_date(competition['date'])
        start_time = format_time_from_date(competition['date'])
        venue = game_info['venue']['fullName']
        city = game_info['venue']['address']['city']
        state = game_info['venue']['address']['state'] if 'state' in game_info['venue']['address'] else ''
        attendance = game_info['attendance'] if completed else 0
        attendance = f'{attendance:,}'

        # Team info
        home_team = self._parse_competitor(home_team_obj)
        away_team = self._parse_competitor(away_team_obj)

        n_regulation_periods = response['format']['regulation']['periods']
        regulation_periods_list = [n for n in range(1, n_regulation_periods + 1)]
        n_extra_periods = len(home_team['linescores']) - n_regulation_periods if len(home_team['linescores']) > n_regulation_periods else 0
        extra_periods_list = []
        if n_extra_periods >= 1:
            if league == 'MLB':
                extra_periods_list = [n for n in range(10, 10 + n_extra_periods)]
            else:
                if n_extra_periods == 1:
                    extra_periods_list = ['OT']
                else:
                    extra_periods_list = [f'OT{n}' for n in range(1, n_extra_periods + 1)]

        fmt = {
            'n_regulation_periods': n_regulation_periods,
            'regulation_periods_list': regulation_periods_list,
            'n_extra_periods': n_extra_periods,
            'extra_periods_list': extra_periods_list,
            'periods_list': regulation_periods_list + extra_periods_list
        }

        # Winner
        game_winner = 'home' if home_team['winner'] else 'away' if away_team['winner'] else None

        # Final game object
        game_info = {
            'date': date,
            'start_time': start_time,
            'venue': venue,
            'city': city,
            'state': state,
            'status': status_display,
            'in_progress': in_progress,
            'completed': completed,
            'attendance': attendance,
            'league': league_obj,
            'season': season_obj,
            'home_team': home_team,
            'away_team': away_team,
            'winner': game_winner,
            'format': fmt
        }

        return game_info

    def get_game_info_OLD(self, league: str, event_id: int):
        ## Hit API
        base_url = self._get_site_api_espn_base_url(league=league)
        event_url = f'{base_url}/summary?event={event_id}'
        response = self._api_call(event_url)

        ## General game info
        
        # Get league info
        league_obj = self.get_league_info(league=league)

        # Season
        season_obj = {
            'year': response['header']['season']['year'],
            'type': response['header']['season']['type']
        }

        # Objects
        game_info = response['game_info']
        competition = response['header']['competitions'][0]
        home_team_obj = competition['competitors'][0]
        away_team_obj = competition['competitors'][1]

        # Status
        status = competition['status']['type']['name']
        status_display = competition['status']['type']['shortDetail']
        completed = competition['status']['type']['completed']

        # Competition info
        date = format_date_from_date(competition['date'])
        start_time = format_time_from_date(competition['date'])
        venue = game_info['venue']['fullName']
        city = game_info['venue']['address']['city']
        state = game_info['venue']['address']['state'] if 'state' in game_info['venue']['address'] else ''
        attendance = game_info['attendance'] if completed else 0
        attendance = f'{attendance:,}'
        
        # Home team info
        home_team_id = int(home_team_obj['team']['id'])
        home_team = {
            'id': home_team_id,
            'name': home_team_obj['team']['name'],
            'logo_url': home_team_obj['team']['logos'][0]['href'],
            'winner': False,
        }

        # Away team info
        away_team_id = int(away_team_obj['team']['id'])
        away_team = {
            'id': away_team_id,
            'name': away_team_obj['team']['name'],
            'logo_url': away_team_obj['team']['logos'][0]['href'],
            'winner': False,
        }

        game_winner = None
        if completed:
            # Home team scores
            home_team['winner'] = home_team_obj['winner']

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
            away_team['winner'] = away_team_obj['winner']

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

        # Final game object
        game_info = {
            'date': date,
            'start_time': start_time,
            'venue': venue,
            'city': city,
            'state': state,
            'in_progress': status_display,
            'completed': completed,
            'attendance': attendance,
            'league': league_obj,
            'season': season_obj,
            'home_team': home_team,
            'away_team': away_team,
            'winner': game_winner
        }

        return game_info
    

    ''' Helpers '''

    def _get_site_api_espn_base_url(self, league):
        sport = LEAGUES[league]['sport']
        code = LEAGUES[league]['code']

        return f'http://site.api.espn.com/apis/site/v2/sports/{sport}/{code}'
    
    def _get_sports_core_api_espn_base_url(self, league):
        sport = LEAGUES[league]['sport']
        code = LEAGUES[league]['code']

        return f'https://sports.core.api.espn.com/v2/sports/{sport}/leagues/{code}'
    
    def _get_partners_api_espn_base_url(self, league: str):
        sport = LEAGUES[league]['sport']
        code = LEAGUES[league]['code']

        return f'https://partners.api.espn.com/v2/sports/{sport}/{code}'

    def _get_scoreboard_url(self, league: str, date_str: str):
        base_url = self._get_site_api_espn_base_url(league)

        url = f'{base_url}/scoreboard?dates={date_str}'
        if league == 'MCBB':
            url += '&group=50'
        
        return url
    
    def _get_scoreboard_header_url():
        return 'https://site.web.api.espn.com/apis/v2/scoreboard/header'
    
    def _api_call(self, url: str):
        print(f' ---------------------- API CALL ----------------------')
        print(url)
        return requests.get(url).json()

    def _parse_competitor(self, competitor):
        
        team = competitor['team']

        # name
        name = ''
        if 'name' in team:
            name = team['name']
        elif 'shortDisplayName' in team:
            name = team['shortDisplayName']

        # Logo
        logo = ''
        if 'logos' in team and len(team['logos']) > 0:
            logo = team['logos'][0]['href']
        elif 'logo' in team:
            logo = team['logo']

        # Winner
        winner = competitor['winner'] if 'winner' in competitor else None

        # Score
        score = 0
        if 'score' in competitor:
            if type(competitor['score']) == dict: 
                score = int(competitor['score']['value'])
            elif type(competitor['score']) == int or type(competitor['score']) == float or type(competitor['score']) == str:
                score = int(competitor['score'])
        
        # Linescores
        line_scores = competitor['linescores'] if 'linescores' in competitor else []

        # Return obj
        d = {
            'id': competitor['id'],
            'name': name,
            'abbreviation': competitor['team']['abbreviation'],
            'display_name': competitor['team']['displayName'],
            'logo_url': logo,
            'winner': winner,
            'score': score,
            'linescores': line_scores
        }

        return d
    
    def _parse_event(self, event: dict):
        
        # Important objects
        competition = event['competitions'][0]
        season = event['season']

        # Season info
        season_obj = {
            'year': season['year'],
            'type': '',
            'name': ''
        }
        if 'seasonType' in event:
            season_obj['type'] = event['seasonType']['type']
            season_obj['name'] = event['seasonType']['name']
        else:
            season_obj['type'] = season['type']

        # Game info
        event_id = event['id']
        event_name = event['shortName']
        dt = format_datetime_from_date(event['date'])
        date = format_date_from_date(event['date'])
        time = format_time_from_date(event['date'])
        headline = competition['notes'][0]['headline'] if competition['notes'] else ''
        
        # Status
        status = competition['status']['type']['name']
        status_display = competition['status']['type']['shortDetail']
        in_progress = (status == 'STATUS_IN_PROGRESS')
        completed = competition['status']['type']['completed']
        
        # Team info
        home_team = self._parse_competitor(competition['competitors'][0])
        away_team = self._parse_competitor(competition['competitors'][1])

        # Score / Result
        result = None
        if completed:
            result = 'home' if home_team['winner'] else 'away' if away_team['winner'] else 'tie'
        
        # Return obj
        game_dict = {
            'event_id': event_id,
            'name': event_name,
            'datetime': dt,
            'date': date,
            'time': time,
            'season': season_obj,
            'headline': headline,
            'status': status_display,
            'in_progress': in_progress,
            'completed': completed,
            'home_team': home_team,
            'away_team': away_team,
            'result': result,
        }
        
        return game_dict
