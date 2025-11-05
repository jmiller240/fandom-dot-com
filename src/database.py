
from flask_login import UserMixin

# Example User class (should inherit from UserMixin)
class User(UserMixin):
    def __init__(self, id, username, password, name):
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.selected_teams = []

    def get_id(self):
        return str(self.id)
    
    def set_selected_teams(self, teams: list):
        self.selected_teams = teams

USERS = {
    1: User(1, 'horse', 'horseman', 'Horse'),
    2: User(2, 'neigh', 'neighman', 'Joe'),
    3: User(3, 'pony', 'ponyboy', 'Phil'),
}
