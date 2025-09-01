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
import pprint

app = Flask(__name__)


''' Constants '''


nfl_teams = pd.read_csv('data/nfl_team_info.csv')
nba_teams = pd.read_csv('data/nba_team_info.csv')
TEAMS_DF = pd.concat([nfl_teams, nba_teams]).reset_index(drop=True)
TEAMS_DF['app-id'] = TEAMS_DF.index

LEAGUES = TEAMS_DF['league'].unique().tolist()
TEAMS = TEAMS_DF[['app-id', 'league', 'id', 'name']].to_dict(orient='records')

TEAMS_OBJ = {league: list(filter(lambda x: x['league'] == league, TEAMS)) for league in LEAGUES}
pprint.pprint(TEAMS_OBJ)
# input()

NFL_LOGO = 'https://a.espncdn.com/i/teamlogos/leagues/500/nfl.png'

NFL_LEAGUE_OBJ = {
    'name': 'NFL',
    'logo-url': 'https://a.espncdn.com/i/teamlogos/leagues/500/nfl.png'
}
NBA_LEAGUE_OBJ = {
    'name': 'NBA',
    'logo-url': 'https://a.espncdn.com/i/teamlogos/leagues/500/nba.png'
}


''' Helpers '''

def get_team_info_url(league: str, team_id: int):
    if league == 'NFL':
        return f'https://partners.api.espn.com/v2/sports/football/nfl/teams/{team_id}'
    else:
        return f'https://partners.api.espn.com/v2/sports/basketball/nba/teams/{team_id}'

def get_team_schedule_url(league: str, team_id: int):
    if league == 'NFL':
        # return f'https://partners.api.espn.com/v2/sports/football/nfl/teams/{team_id}/events?season=2025&limit=1000'
        return f'http://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/11/schedule?season=2025'
    else:
        return f'https://partners.api.espn.com/v2/sports/basketball/nba/teams/{team_id}/events?season=2025&limit=1000'

def get_game_result_url(league: str, event_id: int):
    if league == 'NFL':
        return f'http://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={event_id}'
    else:
        return f'http://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={event_id}'


def return_home_page():
    return render_template('home.html', leagues=LEAGUES, teams=TEAMS_OBJ)

def get_team_league(app_id: int):
    league = TEAMS_DF.loc[TEAMS_DF['app-id'].astype(int) == app_id, 'league'].values[0]
    return league

def get_team_id(app_id: int):
    i = TEAMS_DF.loc[TEAMS_DF['app-id'].astype(int) == app_id, 'id'].values[0]
    return i

# def get_team_id(team_name: str):
#     team_id = TEAMS_DF.loc[TEAMS_DF['name'] == team_name, 'id'].values[0]
#     return int(team_id)

def get_team_name(league: str, id: int):
    name = TEAMS_DF.loc[(TEAMS_DF['league'] == league) & 
                        (TEAMS_DF['id'].astype(int) == id), 'name'].values[0]
    return name

def get_team_full_name(league: str, id: int):
    full_name = TEAMS_DF.loc[(TEAMS_DF['league'] == league) & 
                             (TEAMS_DF['id'].astype(int) == id), 'displayName'].values[0]
    return full_name

def get_team_logo_url(league: str, id: int):
    team_logo_url = TEAMS_DF.loc[(TEAMS_DF['league'].astype(str) == league) & 
                                 (TEAMS_DF['id'].astype(int) == id), 'logoURL'].values[0]
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
        # league = request.form['league']
        # team_id = request.form['team-id']
        team_app_id = request.form['team-id']

        # if not league or not team_id:
        if not team_app_id:
            return return_home_page()
        
        team_app_id = int(team_app_id)
        league = get_team_league(app_id=team_app_id)
        team_id = get_team_id(app_id=team_app_id)

        return redirect(url_for('team_page', league=league, team_id=team_id))

@app.route("/<league>/team/<team_id>")
def team_page(league: str, team_id: int):
    print(league)

    team_id = int(team_id)
    print(team_id)

    league_obj = NFL_LEAGUE_OBJ if league == 'NFL' else NBA_LEAGUE_OBJ

    ## Get team info
    team_name = get_team_name(league=league, id=team_id)
    full_name = get_team_full_name(league=league, id=team_id)
    logo_url = get_team_logo_url(league=league, id=team_id)

    team_obj = {
        'id': team_id,
        'name': team_name,
        'full-name': full_name,
        'logo-url': logo_url,
        'league': league_obj
    }

    ## Get record
    team_info_url = get_team_info_url(league=league, team_id=team_id)
    response = requests.get(team_info_url).json()
    team_record = {
        'Overall': response['team']['record'][0]['displayValue'] if response['team']['record'] else "",
        'Home': response['team']['record'][1]['displayValue'] if response['team']['record'] else "",
        'Away': response['team']['record'][2]['displayValue'] if response['team']['record'] else "",
        'Division': response['team']['record'][3]['displayValue'] if response['team']['record'] else "",
        'Conference': response['team']['record'][4]['displayValue'] if response['team']['record'] else "",
    }

    ## Get schedule
    team_schedule_url = get_team_schedule_url(league=league, team_id=team_id)
    response = requests.get(team_schedule_url)
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

        if home_team_id not in TEAMS_DF['id'].tolist() or away_team_id not in TEAMS_DF['id'].tolist():
            continue

        home_team_logo = get_team_logo_url(league=league, id=home_team_id)
        away_team_logo = get_team_logo_url(league=league, id=away_team_id)

        result = None
        home_team_score = None
        away_team_score = None
        if completed:
            result = 'home' if home_team['score']['winner'] else 'away' if away_team['score']['winner'] else 'tie'
            selected_team_result = 'tie' if result == 'tie' else 'win' if ((result == 'home' and selected_team_is_home) or (result == 'away' and not selected_team_is_home)) else 'loss'
            home_team_score = int(home_team['score']['value'])
            away_team_score = int(away_team['score']['value'])
            game_score_string = str(away_team_score) + " - " + str(home_team_score)

        game_dict = {
            'event_id': event_id,
            'date': date,
            'time': time,
            'league': league_obj,
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

    # with open('data/games.txt', 'w+') as file:
    #     file.write(json.dumps(games))

    # games = []
    # with open('data/games.txt', 'r+') as file:
    #     games = json.load(file)

    return render_template('team-page.html', team=team_obj, team_record=team_record, games_list=games)

@app.route("/<league>/boxscore/<event_id>")
def box_score(league: str, event_id: int):
    ## Hit API
    game_result_url = get_game_result_url(league=league, event_id=event_id)
    response = requests.get(game_result_url).json()
    
    ## General game info
    league_obj = NFL_LEAGUE_OBJ if league == 'NFL' else NBA_LEAGUE_OBJ

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
        'logo_url': get_team_logo_url(league=league, id=home_team_id),
        'winner': False,
    }

    ## Away team info
    away_team_obj = competition['competitors'][1]
    away_team_id = int(away_team_obj['team']['id'])
    away_team = {
        'id': away_team_id,
        'name': away_team_obj['team']['name'],
        'logo_url': get_team_logo_url(league=league, id=away_team_id),
        'winner': False,
    }

    if game_completed:
        # Home team scores
        home_team_score_obj = home_team_obj['linescores']
        home_team['winner'] = home_team_obj['winner'],
        home_team['score'] = {
            'Q1': home_team_score_obj[0]['displayValue'],
            'Q2': home_team_score_obj[1]['displayValue'],
            'Q3': home_team_score_obj[2]['displayValue'],
            'Q4': home_team_score_obj[3]['displayValue'],
            'Total': home_team_obj['score']
        }

        # Away team scores
        away_team_score_obj = away_team_obj['linescores']
        away_team['winner'] = away_team_obj['winner'],
        away_team['score'] = {
            'Q1': away_team_score_obj[0]['displayValue'],
            'Q2': away_team_score_obj[1]['displayValue'],
            'Q3': away_team_score_obj[2]['displayValue'],
            'Q4': away_team_score_obj[3]['displayValue'],
            'Total': away_team_obj['score']
        }

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
        'home-team': home_team,
        'away-team': away_team,
        'winner': game_winner
    }

    return render_template('game-page.html', game_info=game_info)
