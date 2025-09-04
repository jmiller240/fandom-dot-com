import pandas as pd
import pprint

from fandom_dot_com.services.ESPNAPIService import ESPNAPIService



nfl_teams = pd.read_csv('data/nfl_team_info.csv')
nba_teams = pd.read_csv('data/nba_team_info.csv')
TEAMS_DF = pd.concat([nfl_teams, nba_teams]).reset_index(drop=True)
TEAMS_DF['app-id'] = TEAMS_DF.index

service = ESPNAPIService(teams_df=TEAMS_DF)
# games = service.get_team_schedule('CFB', 84, 2024)

game_info = service.get_game_info('NBA', '401716965')

pprint.pprint(game_info)