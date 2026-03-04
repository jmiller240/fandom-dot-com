
import requests
import pandas as pd

LEAGUE_MAPPER = {
    'NFL': {
        'sport': 'football',
        'code': 'nfl'
    },
    'NBA': {
        'sport': 'basketball',
        'code': 'nba'
    },
    'MLB': {
        'sport': 'baseball',
        'code': 'mlb'
    },
    'NHL': {
        'sport': 'hockey',
        'code': 'nhl'
    },
    'CFB': {
        'sport': 'football',
        'code': 'college-football'
    },
    'MCBB': {
        'sport': 'basketball',
        'code': 'mens-college-basketball'
    },
    'WCBB': {
        'sport': 'basketball',
        'code': 'womens-college-basketball'
    },
    'ENG': {
        'sport': 'soccer',
        'code': 'eng.1'
    },
    'ESP': {
        'sport': 'soccer',
        'code': 'esp.1'
    },
    'GER': {
        'sport': 'soccer',
        'code': 'ger.1'
    },
    'ITA': {
        'sport': 'soccer',
        'code': 'ita.1'
    },
    'FRA': {
        'sport': 'soccer',
        'code': 'fra.1'
    },
    'MLS': {
        'sport': 'soccer',
        'code': 'usa.1'
    },
    'UCL': {
        'sport': 'soccer',
        'code': 'uefa.champions'
    },
}


def get_sports_core_api_espn_base_url(league):

    sport = LEAGUE_MAPPER[league]['sport']
    code = LEAGUE_MAPPER[league]['code']

    return f'https://sports.core.api.espn.com/v2/sports/{sport}/leagues/{code}'

def get_league_info(league):
    print(f'{league}')

    base_url = get_sports_core_api_espn_base_url(league=league)
    response = requests.get(base_url).json()

    league_info = {
        'league_id': response['id'],
        'name': league,
        'logo_url': response['logos'][0]['href'],
        'current_season': response['season']['year'],
        'current_season_type': response['season']['type']['type']
    }

    return league_info

leagues = []
for league in LEAGUE_MAPPER.keys():
    info = get_league_info(league)

    leagues.append(info)

leagues_df = pd.DataFrame.from_records(leagues)
print(leagues_df.to_string())
leagues_df.to_csv('leagues_df.csv', index=False)