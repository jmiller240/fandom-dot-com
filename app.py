from flask import Flask, render_template, request, redirect, url_for
import os
import requests
import pandas as pd


app = Flask(__name__)

TEAMS_DF = pd.read_csv('data/team_info.csv')
TEAMS_LIST = TEAMS_DF['name'].tolist()


''' Helpers '''

def return_home_page():
    return render_template('home.html', teams_list=TEAMS_LIST)

def get_team_id(team_name: str):
    team_id = TEAMS_DF.loc[TEAMS_DF['name'] == team_name, 'id'].values[0]
    return team_id

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
    TEAMS_BASE_URL = 'https://partners.api.espn.com/v2/sports/football/nfl/teams'

    team_id = get_team_id(team_name=team)
    print(team_id)

    response = requests.get(f'{TEAMS_BASE_URL}/{team_id}')
    logo_url = response.json()['team']['logos'][0]['href']
    
    return render_template('team-schedule.html', team=team, team_logo_url=logo_url)

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