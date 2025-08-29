'''
TODO:
 - Show results
 - Arrow next to next game
'''

from flask import Flask, render_template, request, redirect, url_for
import os
import requests
import pandas as pd
from datetime import datetime
import pytz
import json

app = Flask(__name__)


''' Constants '''

TEAMS_BASE_URL = 'https://partners.api.espn.com/v2/sports/football/nfl/teams'


TEAMS_DF = pd.read_csv('data/team_info.csv')
TEAMS_LIST = TEAMS_DF['name'].tolist()

NFL_LOGO = 'https://a.espncdn.com/i/teamlogos/leagues/500/nfl.png'


''' Helpers '''

def return_home_page():
    return render_template('home.html', teams_list=TEAMS_LIST)

def get_team_id(team_name: str):
    team_id = TEAMS_DF.loc[TEAMS_DF['name'] == team_name, 'id'].values[0]
    return int(team_id)

def get_team_full_name(id: str):
    full_name = TEAMS_DF.loc[TEAMS_DF['id'].astype(int) == id, 'displayName'].values[0]
    return full_name

def get_team_logo_url(id: int):
    team_logo_url = TEAMS_DF.loc[TEAMS_DF['id'].astype(int) == id, 'logoURL'].values[0]
    return team_logo_url

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


''' Routes '''

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return return_home_page()
    elif request.method == 'POST':
        team = request.form['team']
        if not team:
            return return_home_page()
        return redirect(url_for('team_schedule', team=team))

@app.route("/team/<team>")
def team_schedule(team: str):
    ## Get team ID
    team_id = get_team_id(team_name=team)
    full_name = get_team_full_name(id=team_id)
    print(team_id)

    ## Get logo
    # response = requests.get(f'{TEAMS_BASE_URL}/{team_id}')
    # logo_url = response.json()['team']['logos'][0]['href']
    logo_url = get_team_logo_url(team_id)

    ## Get record
    response = requests.get(f'{TEAMS_BASE_URL}/{team_id}').json()
    team_record = {
        'Overall': response['team']['record'][0]['displayValue'],
        'Home': response['team']['record'][1]['displayValue'],
        'Away': response['team']['record'][2]['displayValue'],
        'Division': response['team']['record'][3]['displayValue'],
        'Conference': response['team']['record'][4]['displayValue'],
    }

    ## Get schedule
    TEAMS_SCHEDULE_URL = f'https://partners.api.espn.com/v2/sports/football/nfl/teams/{team_id}/events?season=2025'
    response = requests.get(TEAMS_SCHEDULE_URL)
    events = response.json()['events']

    games = []
    for game in events:
        event_id = game['id']
        date = format_date_from_date(game['date'])
        time = format_time_from_date(game['date'])
        competition = game['competitions'][0]
        completed = competition['status']['type']['completed']
        home_team = competition['competitors'][0]
        away_team = competition['competitors'][1]

        # Get home team logo
        home_team_id = int(home_team['id'])    
        away_team_id = int(away_team['id'])
        selected_team_is_home = team_id == home_team_id

        home_team_logo = get_team_logo_url(home_team_id)
        away_team_logo = get_team_logo_url(away_team_id)

        result = None
        home_team_score = None
        away_team_score = None
        if completed:
            result = 'home' if home_team['score']['winner'] else 'away' if away_team['score']['winner'] else 'tie'
            # selected_team_winner = (winner == 'home' and team_id == home_team_id) or (winner == 'away' and team_id == away_team_id)
            selected_team_result = 'tie' if result == 'tie' else 'win' if ((result == 'home' and selected_team_is_home) or (result == 'away' and not selected_team_is_home)) else 'loss'
            home_team_score = int(home_team['score']['value'])
            away_team_score = int(away_team['score']['value'])
            game_score_string = str(away_team_score) + " - " + str(home_team_score)


        game_dict = {
            'event_id': event_id,
            'date': date,
            'time': time,
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
        print(game_dict)
        games.append(game_dict)

    # with open('data/games.txt', 'w+') as file:
    #     file.write(json.dumps(games))

    # games = []
    # with open('data/games.txt', 'r+') as file:
    #     games = json.load(file)

    return render_template('team-schedule.html', team=team, team_full_name=full_name, team_logo_url=logo_url, team_record=team_record, games_list=games)

@app.route("/boxscore/<event_id>")
def box_score(event_id: int):
    EVENT_BASE_URL = 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/summary'
    response = requests.get(f'{EVENT_BASE_URL}?event={event_id}').json()
    
    ## General game info
    competition = response['header']['competitions'][0]
    date = format_date_from_date(competition['date'])
    start_time = format_time_from_date(competition['date'])
    venue = response['gameInfo']['venue']['fullName']
    city = response['gameInfo']['venue']['address']['city']
    state = response['gameInfo']['venue']['address']['state']
    attendance = response['gameInfo']['attendance']

    league = {
        'name': 'NFL',
        'logo_url': 'https://a.espncdn.com/i/teamlogos/leagues/500/nfl.png'
    }
    home_team_obj = competition['competitors'][0]
    home_team_id = int(home_team_obj['team']['id'])
    home_team_score_obj = home_team_obj['linescores']
    home_team = {
        'id': home_team_id,
        'name': home_team_obj['team']['name'],
        'logo_url': get_team_logo_url(home_team_id),
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
    away_team_id = int(away_team_obj['team']['id'])
    away_team_score_obj = away_team_obj['linescores']
    away_team = {
        'id': away_team_id,
        'name': away_team_obj['team']['name'],
        'logo_url': get_team_logo_url(away_team_id),
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
        'league': league,
        'home-team': home_team,
        'away-team': away_team,
        'winner': 'home' if home_team['winner'] else 'away'
    }

    return render_template('game-page.html', game_info=game_info)

@app.route("/hi", methods=['GET', 'POST'])
def suk_home():
    if request.method == 'GET':
        return render_template('suk/suk-home.html')
    elif request.method == 'POST':
        name = request.form['name']
        if not name:
            return render_template('suk/suk-home.html')
        return redirect(url_for('suk', name=name))

@app.route("/suk/<name>")
def suk(name: str):
    return render_template('suk/suk.html', name=name)

@app.route("/base")
def base():
    return render_template('base.html')