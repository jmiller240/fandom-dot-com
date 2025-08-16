import requests
from pprint import pprint
import pandas as pd


TEAMS_BASE_URL = 'https://partners.api.espn.com/v2/sports/football/nfl/teams'
TEAM_ID = 11

response = requests.get(f'{TEAMS_BASE_URL}/{TEAM_ID}')

d = response.json()

logo_url = d['team']['logos'][0]
print(logo_url)
