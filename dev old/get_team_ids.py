import requests
from pprint import pprint
import pandas as pd


LEAGUES_MAPPER = {
    'NFL': {
        'sport': 'football',
        'name': 'nfl',
    },
    'CFB': {
        'sport': 'football',
        'name': 'college-football',
    },
    'NBA': {
        'sport': 'basketball',
        'name': 'nba',
    },
    # 'MBB': {
    #     'sport': 'basketball',
    #     'name': 'mens-college-basketball',
    # },
    # 'WBB': {
    #     'sport': 'basketball',
    #     'name': 'womens-college-basketball',
    # },
    'MLB': {
        'sport': 'baseball',
        'name': 'mlb',
    },
    'PREM': {
        'sport': 'soccer',
        'name': 'eng.1',
    }
}


KEYS = ['id', 'displayName', 'location', 'name', 'shortDisplayName', 'abbreviation', 'color', 'alternateColor']

def get_info_as_df(league, sport, name):
    base_url = f'https://partners.api.espn.com/v2/sports/{sport}/{name}/teams'
    response = requests.get(f'{base_url}?limit=1000').json()
    teams_list = response['teams']

    # Loop teams and create dict
    teams_dict = []
    for team_obj in teams_list:
        team_d = {}
        for key in KEYS:
            if key in team_obj.keys():
                team_d[key] = team_obj[key]
            else:
                team_d[key] = ''
            
        teams_dict.append(team_d)

    # Create df from dict
    teams_df = pd.DataFrame.from_records(data=teams_dict)
    teams_df['id'] = teams_df['id'].astype(int)

    def get_team_logo_url(id: int):
        response = requests.get(f'{base_url}/{id}')
        d = response.json()
        logos = d['team']['logos']
        primary_url = logos[0]['href']
        return primary_url

    teams_df['logoURL'] = teams_df['id'].apply(lambda x: get_team_logo_url(x))
    teams_df = teams_df.sort_values(by='id', ascending=True).reset_index(drop=True)
    teams_df['league'] = league

    teams_df.to_csv(f'data/{league}_teams_info.csv', index=False)


for league,d in LEAGUES_MAPPER.items():
    print(f'League: {league}')
    get_info_as_df(league=league, sport=d['sport'], name=d['name'])


master_df = pd.DataFrame(columns=['id', 'displayName', 'location', 'name', 'shortDisplayName', 'abbreviation', 'color', 'alternateColor'])
for league in LEAGUES_MAPPER.keys():
    df = pd.read_csv(f'data/{league}_teams_info.csv')

    master_df = pd.concat([master_df, df]).reset_index(drop=True)

master_df['app-id'] = master_df.index
master_df.to_csv('data/teams_df.csv', index=False)