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

from src.models import League, Team, Account
from src.extensions import db

from ..helpers.functions import format_date_from_date, format_time_from_date
from ..services.ESPNAPIService import ESPNAPIService
from ..services.DatabaseService import DatabaseService

''' Constants '''

SEASONS = [i for i in range(2018, 2025)]
DEFAULT_SEASON = 2025


ESPNService = ESPNAPIService()
DBService = DatabaseService()

# Init blueprint
core_bp = Blueprint("core", __name__)



''' Routes '''

@core_bp.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('accounts.login'))
    
    # if not current_user.teams:
    #     return redirect(url_for('core.team_selection'))

    return redirect(url_for('core.home'))


def return_team_selection_page(selected_team_ids: list = []):
    # Get leagues and teams
    all_leagues = DBService.get_leagues()
    league_names = [league.name for league in all_leagues]
    
    # Format to dict of league / team list pairs
    teams_ob = {}
    for league in all_leagues:
        league_teams: list[Team] = league.teams
        league_teams = [{'id': team.id, 'name': team.name, 'logo_url': team.logo_url} for team in league_teams]

        teams_ob[league.name] = league_teams

    return render_template('team-selection.html', league_names=league_names, teams=teams_ob, selected_team_ids=selected_team_ids)


@core_bp.route("/team-selection", methods=['GET', 'POST'])
@login_required
def team_selection():
    # Get user teams from DB (if any)
    user_teams: list[Team] = current_user.teams
    user_team_ids = [t.id for t in user_teams]

    ## Return the page
    if request.method == 'GET':
        return return_team_selection_page(user_team_ids)
    
    ## Process the submission
    elif request.method == 'POST':
        # Get selected teams from form
        form_team_ids = request.form.getlist('selected-teams')
        if not form_team_ids:
            return return_team_selection_page(user_team_ids)

        ## Process selections ##
        form_team_ids = [int(i) for i in form_team_ids]      
        
        # Add new teams to DB
        for i in form_team_ids:
            print(f'team {i}')
            
            # Get info from DB
            # t: Team = Team.query.filter_by(id=i).first()
            t = DBService.get_team(id=i)

            # Insert to DB
            if i in user_team_ids:
                print(f'Ignoring {t.id}, already added.')
                continue
            else:
                print(f'Adding {t.id}.')   
                current_user.teams.append(t)
                db.session.commit()
            
        # Remove any *unselected* teams
        for i in user_team_ids:
            if i not in form_team_ids:
                # Get info from DB
                # t: Team = Team.query.filter_by(id=i).first()
                t = DBService.get_team(id=i)

                print(f'Removing {t.id}')
                current_user.teams.remove(t)
                db.session.commit()

        return redirect(url_for('core.home'))


def get_team_info(team: Team):
    # Team info
    team_info = {
        'espn_id': team.espn_team_id,
        'name': team.name,
        'display_name': team.display_name,
        'logo_url': team.logo_url
    }

    # League info
    league: League = team.league #DBService.get_league(team.league_id)
    league_info = {
        'espn_id': league.espn_league_id,
        'name': league.name,
        'logo_url': league.logo_url,
        'current_season': league.current_season,
        'current_season_type': league.current_season_type
    }
    team_info['league'] = league_info

    # Record
    team_record = ESPNService.get_team_record(league=league.name, team_id=team.espn_team_id, season=league.current_season)
    team_info['record'] = team_record

    return team_info


@core_bp.route("/home")
@login_required
def home():
    # Get user teams
    user_teams: list[Team] = current_user.teams
    # if not user_teams:
    #     return redirect(url_for('core.team_selection'))

    # Get games
    master_teams_info = []
    master_games = []
    season = DEFAULT_SEASON

    for team in user_teams:
        print(team)

        # League
        # season = ESPNService.get_league_current_season(league=league)
        # league_obj = ESPNService.get_league_info(league=league)
        # season = int(league_obj['season']['year'])

        # Get team info
        # team_info = ESPNService.get_team_info(league=league_name, team_id=espn_team_id, season=current_season)
        team_info = get_team_info(team=team)
        league = DBService.get_league(team.league_id)

        # Get schedule
        games = ESPNService.get_team_schedule(league=league.name, team_id=team.espn_team_id, season=league.current_season)

        master_teams_info.append(team_info)
        master_games.extend(games)

    master_games = sorted(master_games, key=lambda game: game['datetime'])

    # pprint.pprint(master_games[:5])

    return render_template('home.html', teams_list=master_teams_info, games_list=master_games, season=season)


@core_bp.route("/<league>/team/<team_id>/season/<season>")
def team_page(league: str, team_id: int, season: int):
    team_id = int(team_id)
    season = int(season)

    ## Query DB
    league_obj: League = League.query.filter_by(name=league).first()
    team = Team.query.filter_by(espn_team_id=team_id, league_id=league_obj.id).first()

    ## Format team info
    # team_info = ESPNService.get_team_info(league=league, team_id=team_id, season=season)
    team_info = get_team_info(team=team)

    ## Get schedule
    games = ESPNService.get_team_schedule(league=league, team_id=team_id, season=season)

    return render_template('team-page.html', team=team_info, games_list=games, season=season, seasons=SEASONS)


@core_bp.route("/<league>/boxscore/<event_id>")
def box_score(league: str, event_id: int):
    # Hit API
    game_info = ESPNService.get_game_info(league=league, event_id=event_id)

    return render_template('game-page.html', game_info=game_info)
