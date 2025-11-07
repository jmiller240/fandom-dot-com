'''
TODO:
 - Show results
 - Arrow next to next game
'''

from flask import Flask, session, render_template, request, redirect, url_for, Blueprint
from flask_login import login_required, current_user
import os
import requests
import pandas as pd
from datetime import datetime
import pytz
import json
import pprint

# from ..database import USERS, User
from src.models import Team, Account
from src.extensions import db

from ..helpers.functions import format_date_from_date, format_time_from_date
from ..services.ESPNAPIService import ESPNAPIService


''' Constants '''


# nfl_teams = pd.read_csv('data/nfl_team_info.csv')
# nba_teams = pd.read_csv('data/nba_team_info.csv')
# TEAMS_DF = pd.concat([nfl_teams, nba_teams]).reset_index(drop=True)
# TEAMS_DF['appID'] = TEAMS_DF.index

TEAMS_DF = pd.read_csv('data/teams_df.csv')
TEAMS_DF['is-selected-team'] = False

LEAGUES = TEAMS_DF['league'].unique().tolist()
TEAMS = TEAMS_DF[['appID', 'is-selected-team', 'league', 'id', 'name', 'logoURL']].to_dict(orient='records')

TEAMS_OBJ = {league: list(filter(lambda x: x['league'] == league, TEAMS)) for league in LEAGUES}
# pprint.pprint(TEAMS_OBJ)


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


def get_team_league(app_id: int) -> str:
    league = TEAMS_DF.loc[TEAMS_DF['appID'].astype(int) == app_id, 'league'].values[0]
    return league

def get_team_id(app_id: int) -> int:
    i = TEAMS_DF.loc[TEAMS_DF['appID'].astype(int) == app_id, 'id'].values[0]
    return int(i)

def get_team_name(app_id: int) -> str:
    name = TEAMS_DF.loc[TEAMS_DF['appID'].astype(int) == app_id, 'name'].values[0]
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
    team_logo_url = TEAMS_DF.loc[TEAMS_DF['appID'].astype(int) == app_id, 'logoURL'].values[0]
    return team_logo_url

ESPNService = ESPNAPIService(teams_df=TEAMS_DF)


# Init blueprint
core_bp = Blueprint("core", __name__)



''' Routes '''

@core_bp.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('accounts.login'))
    
    if not current_user.teams:
        return redirect(url_for('core.team_selection'))

    return redirect(url_for('core.home'))


def return_team_selection_page(selected_team_ids: list = []):
    # Get leagues
    leagues = db.session.query(Team.league).distinct().all()
    leagues = [i[0] for i in leagues]

    # Get teams
    all_teams = Team.query.all()
    teams_ob = {}
    for league in leagues:
        league_teams = [t for t in all_teams if t.league == league]
        print(league_teams)

        teams_ob[league] = league_teams

    return render_template('team-selection.html', leagues=leagues, teams=teams_ob, selected_team_ids=selected_team_ids)

@core_bp.route("/team-selection", methods=['GET', 'POST'])
@login_required
def team_selection():
    # Get user teams from DB (if any)
    user_teams: list[Team] = current_user.teams
    user_team_ids = [t.appID for t in user_teams]

    ## Return the page
    if request.method == 'GET':
        return return_team_selection_page(user_team_ids)
    
    ## Process the submission
    elif request.method == 'POST':
        # Get selected teams from form
        form_team_ids = request.form.getlist('selected-teams')
        if not form_team_ids:
            return return_team_selection_page(user_team_ids)

        # Process selections
        form_team_ids = [int(i) for i in form_team_ids]      
        
        teams_obj = []
        for i in form_team_ids:
            print(f'team {i}')
            
            # Get info from DB
            t: Team = Team.query.filter_by(appID=i).first()

            d = {
                'appID': i,
                'id': t.id,
                'name': t.name,
                'league': t.league,
                'logoURL': t.logoURL
            }
            teams_obj.append(d)

            # Insert to DB
            if i in user_team_ids:
                print(f'Ignoring {t.appID}, already added.')
                continue
            else:
                print(f'Adding {t.appID}.')   
                current_user.teams.append(t)
                db.session.commit()
            
        session['selected-teams'] = teams_obj

        # Remove any *unselected* teams
        for i in user_team_ids:
            if i not in form_team_ids:
                # Get info from DB
                t: Team = Team.query.filter_by(appID=i).first()

                print(f'Removing {t.appID}')
                current_user.teams.remove(t)
                db.session.commit()

        return redirect(url_for('core.home'))


@core_bp.route("/home")
@login_required
def home():
    # Get user teams
    user_teams: list[Team] = current_user.teams
    if not user_teams:
        return redirect(url_for('core.team_selection'))

    # Get games
    master_teams_info = []
    master_games = []
    for team in user_teams:
        # Team variables
        league = team.league  
        team_id = team.id 
        season = ESPNService.get_league_current_season(league=league)
        
        # Get team info
        team_info = ESPNService.get_team_info(league=league, team_id=team_id, season=season)

        # Get schedule
        games = ESPNService.get_team_schedule(league=league, team_id=team_id, season=season)

        master_teams_info.append(team_info)
        master_games.extend(games)

    master_games = sorted(master_games, key=lambda game: game['datetime'])

    pprint.pprint(master_games[:5])

    return render_template('home.html', teams_list=master_teams_info, games_list=master_games, season=season)


@core_bp.route("/<league>/team/<team_id>/season/<season>")
def team_page(league: str, team_id: int, season: int):
    team_id = int(team_id)
    season = int(season)

    ## Get team info
    team_info = ESPNService.get_team_info(league=league, team_id=team_id, season=season)

    ## Get schedule
    games = ESPNService.get_team_schedule(league=league, team_id=team_id, season=season)

    return render_template('team-page.html', team=team_info, games_list=games, season=season, seasons=SEASONS)


@core_bp.route("/<league>/boxscore/<event_id>")
def box_score(league: str, event_id: int):
    # Hit API
    game_info = ESPNService.get_game_info(league=league, event_id=event_id)

    return render_template('game-page.html', game_info=game_info)
