
import requests
import pandas as pd


def get_sports_core_api_espn_base_url(league):
    if league == 'NFL':
        return 'https://sports.core.api.espn.com/v2/sports/football/leagues/nfl'
    elif league == 'NBA':
        return 'https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba'
    elif league == 'CFB':
        return 'https://sports.core.api.espn.com/v2/sports/football/leagues/college-football'
    elif league == 'MLB':
        return 'https://sports.core.api.espn.com/v2/sports/baseball/leagues/mlb'
    elif league == 'PREM':
        return 'https://sports.core.api.espn.com/v2/sports/soccer/leagues/eng.1'


leagues = []
for league in ['NFL', 'NBA', 'CFB', 'MLB', 'PREM']:
    base_url = get_sports_core_api_espn_base_url(league=league)
    response = requests.get(base_url).json()

    league_info = {
        'league_id': response['id'],
        'name': league,
        'logo_url': response['logos'][0]['href'],
        'current_season': response['season']['year'],
        'current_season_type': response['season']['type']['type']
    }

    leagues.append(league_info)

leagues_df = pd.DataFrame.from_records(leagues)
print(leagues_df.to_string())
leagues_df.to_csv('data/leagues_df.csv', index=False)