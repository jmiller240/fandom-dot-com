import requests
from pprint import pprint
import pandas as pd
from datetime import datetime
import pytz

''' Functions '''

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


TEAMS_DF = pd.read_csv('data/team_info.csv')


EVENT_ID = 401773003
EVENT_BOXSCORE_BASE_URL = f'http://site.api.espn.com/apis/site/v2/sports/football/nfl/summary'

response = requests.get(f'{EVENT_BOXSCORE_BASE_URL}?event={EVENT_ID}')

d = response.json()

## General game info
competition = d['header']['competitions'][0]
date = format_date_from_date(competition['date'])
start_time = format_time_from_date(competition['date'])
venue = d['gameInfo']['venue']['fullName']
city = d['gameInfo']['venue']['address']['city']
state = d['gameInfo']['venue']['address']['state']
attendance = d['gameInfo']['attendance']

home_team_obj = competition['competitors'][0]
home_team_score_obj = home_team_obj['linescores']
home_team = {
    'id': home_team_obj['team']['id'],
    'name': home_team_obj['team']['name'],
    'winner': home_team_obj['winner'],
    'score': {
        'Q1': home_team_score_obj[0]['displayValue'],
        'Q2': home_team_score_obj[1]['displayValue'],
        'Q3': home_team_score_obj[2]['displayValue'],
        'Q4': home_team_score_obj[3]['displayValue'],
        'Total': home_team_obj['score']
    },
}

away_team_obj = competition['competitors'][1]
away_team_score_obj = away_team_obj['linescores']
away_team = {
    'id': away_team_obj['team']['id'],
    'name': away_team_obj['team']['name'],
    'winner': away_team_obj['winner'],
    'score': {
        'Q1': away_team_score_obj[0]['displayValue'],
        'Q2': away_team_score_obj[1]['displayValue'],
        'Q3': away_team_score_obj[2]['displayValue'],
        'Q4': away_team_score_obj[3]['displayValue'],
        'Total': away_team_obj['score']
    },
}


game_info = {
    'date': date,
    'start-time': start_time,
    'venue': venue,
    'city': city,
    'state': state,
    'attendance': attendance,
    'home-team': home_team,
    'away-team': away_team,
    'winner': 'home' if home_team['winner'] else 'away'
}

pprint(game_info)
