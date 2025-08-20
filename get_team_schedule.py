import requests
from pprint import pprint
import pandas as pd
from datetime import datetime
import pytz

TEAM_ID = 11
TEAMS_SCHEDULE_URL = f'https://partners.api.espn.com/v2/sports/football/nfl/teams/{TEAM_ID}/events?season=2025'

response = requests.get(TEAMS_SCHEDULE_URL)

d = response.json()
pprint(d['events'][0])


def format_date(s: str):
    dt = datetime.fromisoformat(s)
    sdt = datetime.strftime(dt, '%m/%d/%Y')
    
    return sdt

def format_time(s: str):
    dt = datetime.fromisoformat(s)
    
    # 2. Define the target timezone (Central Time)
    central_timezone = pytz.timezone('America/Chicago')

    # 3. Convert the datetime object to the target timezone
    central_datetime = dt.astimezone(central_timezone)
    
    time = central_datetime.strftime("%I:%M %p")
    return time

games = []
games_list = []
dates_list = []
for game in d['events']:
    date = format_date(game['date'])
    time = format_time(game['date'])
    competition = game['competitions'][0]
    completed = competition['status']['type']['completed']
    home_team = competition['competitors'][0]
    away_team = competition['competitors'][1]

    winner = None
    home_team_score = None
    away_team_score = None
    if completed:
        winner = home_team['team']['abbreviation'] if home_team['score']['winner'] else away_team['team']['abbreviation']
        home_team_score = home_team['score']['value']
        away_team_score = away_team['score']['value']

    game_dict = {
        'date': date,
        'dt': game['date'],
        'time': time,
        'completed': completed,
        'home-team': home_team['team']['abbreviation'],
        'home-team-score': home_team_score,
        'away-team': away_team['team']['abbreviation'],
        'away-team-score': away_team_score,
        'winner': winner,
    }
    games_list.append(game['shortName'])
    dates_list.append(game['date'])
    games.append(game_dict)


print(games_list)
print(dates_list)


pprint(games)

# schedule = [f'{format_date(dates_list[i])}: {games_list[i]}' for i in range(len(games_list))]
# pprint(schedule)