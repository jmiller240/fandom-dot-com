import requests
from pprint import pprint
import pandas as pd


TEAMS_BASE_URL = 'https://partners.api.espn.com/v2/sports/basketball/nba/teams'
response = requests.get(TEAMS_BASE_URL)

d = response.json()

# pprint(d)
teams_dict = []

keys = ['id', 'displayName', 'location', 'name', 'shortDisplayName', 'abbreviation', 'color', 'alternateColor']
for team in d['teams']:
    team_d = {}
    for key in keys:
        team_d[key] = team[key]
        
    teams_dict.append(team_d)


teams_df = pd.DataFrame.from_records(data=teams_dict)
teams_df['id'] = teams_df['id'].astype(int)

def get_team_logo_url(id: int):
    response = requests.get(f'{TEAMS_BASE_URL}/{id}')
    d = response.json()
    logos = d['team']['logos']
    primary_url = logos[0]['href']
    return primary_url

teams_df['logoURL'] = teams_df['id'].apply(lambda x: get_team_logo_url(x))

teams_df = teams_df.sort_values(by='id', ascending=True).reset_index(drop=True)

teams_df.to_csv('data/nba_team_info.csv', index=False)