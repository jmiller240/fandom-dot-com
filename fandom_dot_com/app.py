'''
TODO:
 - Show results
 - Arrow next to next game
'''

from flask import Flask, session, render_template, request, redirect, url_for
import os
import requests
import pandas as pd
from datetime import datetime
import pytz
import json
import pprint


from .helpers.functions import format_date_from_date, format_time_from_date
from .services.ESPNAPIService import ESPNAPIService


''' Constants '''


# nfl_teams = pd.read_csv('data/nfl_team_info.csv')
# nba_teams = pd.read_csv('data/nba_team_info.csv')
# TEAMS_DF = pd.concat([nfl_teams, nba_teams]).reset_index(drop=True)
# TEAMS_DF['app-id'] = TEAMS_DF.index

TEAMS_DF = pd.read_csv('data/teams_df.csv')

LEAGUES = TEAMS_DF['league'].unique().tolist()
TEAMS = TEAMS_DF[['app-id', 'league', 'id', 'name', 'logoURL']].to_dict(orient='records')

TEAMS_OBJ = {league: list(filter(lambda x: x['league'] == league, TEAMS)) for league in LEAGUES}
pprint.pprint(TEAMS_OBJ)


# NFL_LOGO = 'https://a.espncdn.com/i/teamlogos/leagues/500/nfl.png'

NFL_LEAGUE_OBJ = {
    'name': 'NFL',
    'logo-url': 'https://a.espncdn.com/i/teamlogos/leagues/500/nfl.png'
}
NBA_LEAGUE_OBJ = {
    'name': 'NBA',
    'logo-url': 'https://a.espncdn.com/i/teamlogos/leagues/500/nba.png'
}

SEASONS = [i for i in range(2018, 2025)]
DEFAULT_SEASON = 2025


''' Helpers '''

def get_team_info_url(league: str, team_id: int):
    if league == 'NFL':
        return f'https://partners.api.espn.com/v2/sports/football/nfl/teams/{team_id}'
    else:
        return f'https://partners.api.espn.com/v2/sports/basketball/nba/teams/{team_id}'

def get_team_schedule_url(league: str, team_id: int):
    if league == 'NFL':
        return f'https://partners.api.espn.com/v2/sports/football/nfl/teams/{team_id}/events?season=2025&limit=1000'
        # return f'http://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/11/schedule?season=2025'
    else:
        return f'https://partners.api.espn.com/v2/sports/basketball/nba/teams/{team_id}/events?season=2025&limit=1000'

def get_game_result_url(league: str, event_id: int):
    if league == 'NFL':
        return f'http://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={event_id}'
    else:
        return f'http://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={event_id}'


def return_home_page():
    return render_template('home.html', leagues=LEAGUES, teams=TEAMS_OBJ)

def get_team_league(app_id: int) -> str:
    league = TEAMS_DF.loc[TEAMS_DF['app-id'].astype(int) == app_id, 'league'].values[0]
    return league

def get_team_id(app_id: int) -> int:
    i = TEAMS_DF.loc[TEAMS_DF['app-id'].astype(int) == app_id, 'id'].values[0]
    return int(i)

def get_team_name(app_id: int) -> str:
    name = TEAMS_DF.loc[TEAMS_DF['app-id'].astype(int) == app_id, 'name'].values[0]
    return name

# def get_team_name(league: str, id: int):
#     name = TEAMS_DF.loc[(TEAMS_DF['league'] == league) & 
#                         (TEAMS_DF['id'].astype(int) == id), 'name'].values[0]
#     return name

def get_team_full_name(league: str, id: int):
    full_name = TEAMS_DF.loc[(TEAMS_DF['league'] == league) & 
                             (TEAMS_DF['id'].astype(int) == id), 'displayName'].values[0]
    return full_name

def get_team_logo_url(app_id: int) -> str:
    team_logo_url = TEAMS_DF.loc[TEAMS_DF['app-id'].astype(int) == app_id, 'logoURL'].values[0]
    return team_logo_url



app = Flask(__name__)
app.secret_key = 'any random string'

ESPNService = ESPNAPIService(teams_df=TEAMS_DF)


''' Routes '''

@app.route("/")
def index():
    if 'username' in session:
        username = session['username']
        if 'selected-teams' in session:
            # Get teams
            teams = session['selected-teams']

            # Return first team page
            team_app_id = int(teams[0]['app-id'])
            league = get_team_league(app_id=team_app_id)
            team_id = get_team_id(app_id=team_app_id)
            league_current_season = ESPNService.get_league_current_season(league=league)

            return redirect(url_for('team_page', league=league, team_id=team_id, season=league_current_season))

        else:
            return render_template('home.html', username=username, leagues=LEAGUES, teams=TEAMS_OBJ)
    else:
        return render_template('login.html')

@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    session['username'] = username
    return redirect(url_for('team_selection', _method='GET'))

@app.route("/logout")
def logout():
    session.clear()
    # if 'username' in session:?one)

    return redirect(url_for('index'))

@app.route("/team-selection", methods=['GET', 'POST'])
def team_selection():
    if request.method == 'GET':
        return return_home_page()
    elif request.method == 'POST':
        # Get list of teams
        team_ids = request.form.getlist('selected-teams')
        if not team_ids:
            return return_home_page()

        team_ids = [int(i) for i in team_ids]

        # Store them in session
        teams_obj = []
        for i in team_ids:
            d = {
                'app-id': i,
                'id': get_team_id(i),
                'name': get_team_name(i),
                'league': get_team_league(i),
                'logoURL': get_team_logo_url(i)
            }
            teams_obj.append(d)

        session['selected-teams'] = teams_obj

        # Return first team page
        team_app_id = team_ids[0]
        
        team_app_id = int(team_app_id)
        league = get_team_league(app_id=team_app_id)
        team_id = get_team_id(app_id=team_app_id)

        league_current_season = ESPNService.get_league_current_season(league=league)

        return redirect(url_for('team_page', league=league, team_id=team_id, season=league_current_season))


@app.route("/<league>/team/<team_id>/season/<season>")
def team_page(league: str, team_id: int, season: int):
    team_id = int(team_id)
    season = int(season)

    ## Get team info
    team_info = ESPNService.get_team_info(league=league, team_id=team_id, season=season)

    ## Get schedule
    games = ESPNService.get_team_schedule(league=league, team_id=team_id, season=season)

    return render_template('team-page.html', team=team_info, games_list=games, season=season, seasons=SEASONS)


@app.route("/<league>/boxscore/<event_id>")
def box_score(league: str, event_id: int):
    # Hit API
    game_info = ESPNService.get_game_info(league=league, event_id=event_id)

    return render_template('game-page.html', game_info=game_info)
