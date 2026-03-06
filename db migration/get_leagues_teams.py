
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
    }
}

TEAM_INFO_MAPPER = {
    'id': 'espn_team_id', 
    'displayName': 'display_name', 
    'location': 'location', 
    'name': 'name', 
    'shortDisplayName': 'short_display_name', 
    'abbreviation': 'abbreviation', 
    'color': 'color', 
    'alternateColor': 'alternate_color'
}


def get_sports_core_api_espn_base_url(league):
    sport = LEAGUE_MAPPER[league]['sport']
    code = LEAGUE_MAPPER[league]['code']

    return f'https://sports.core.api.espn.com/v2/sports/{sport}/leagues/{code}'

def get_partners_api_espn_base_url(league):
    sport = LEAGUE_MAPPER[league]['sport']
    code = LEAGUE_MAPPER[league]['code']

    return f'https://partners.api.espn.com/v2/sports/{sport}/{code}'

def get_league_info(league):
    base_url = get_sports_core_api_espn_base_url(league=league)
    response = requests.get(base_url).json()

    league_info = {
        'espn_league_id': response['id'],
        'name': league,
        'display_name': response['name'],
        'logo_url': response['logos'][0]['href'],
        'current_season': response['season']['year'],
        'current_season_type': response['season']['type']['type']
    }

    return league_info

def get_league_teams_info(league):

    # Base team info

    base_url = get_partners_api_espn_base_url(league)
    url = f'{base_url}/teams?limit=1000'
    response = requests.get(url).json()
    teams = response['teams']

    teams_dict = []
    for team_obj in teams:
        team_d = {
            'league': league
        }

        # Base team info
        for key,col in TEAM_INFO_MAPPER.items():
            if key in team_obj.keys():
                team_d[col] = team_obj[key]
            else:
                team_d[col] = ''
        
        # Logo
        espn_team_id = team_obj['id']
        response = requests.get(f'{base_url}/teams/{espn_team_id}').json()
        logo = response['team']['logos'][0]['href']
        team_d['logo_url'] = logo

        teams_dict.append(team_d)

    return teams_dict

def get_leagues_df():
    # League info
    leagues = []
    for league in LEAGUE_MAPPER.keys():
        print(f'League info: {league}')
        info = get_league_info(league)
        leagues.append(info)

    leagues_df = pd.DataFrame.from_records(leagues)

    return leagues_df

def get_teams_df():
    # Teams
    teams = []
    for league in LEAGUE_MAPPER.keys():
        print(f'Team info: {league}')
        league_teams = get_league_teams_info(league)
        teams.extend(league_teams)
    
    teams_df = pd.DataFrame.from_records(data=teams)

    return teams_df

def main():
    
    # Leagues
    leagues_df = get_leagues_df()
    print(leagues_df.head().to_string())

    # Teams
    teams_df = get_teams_df()
    print(teams_df.head().to_string())

    # Export
    leagues_df.to_csv('leagues_df.csv', index=False)
    teams_df.to_csv('teams_df.csv', index=False)


if __name__ == '__main__':
    main()
