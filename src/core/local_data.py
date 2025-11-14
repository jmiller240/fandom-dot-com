


nfl_teams = pd.read_csv('data/nfl_team_info.csv')
nba_teams = pd.read_csv('data/nba_team_info.csv')
TEAMS_DF = pd.concat([nfl_teams, nba_teams]).reset_index(drop=True)
TEAMS_DF['appID'] = TEAMS_DF.index

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