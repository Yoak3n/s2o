from dotenv import load_dotenv,find_dotenv
from api import get_user_vault
from game import Game
class User:
    def __init__(self):
        self.id = ''
        self.api_key = ''
        self._get_config()
    
    def _get_config(self):
        load_dotenv(verbose=True)
        import os
        self.id = os.getenv('ID')
        self.api_key = os.getenv('API_KEY')
        if not self.id or not self.api_key:
            raise Exception('ID and API_KEY must be set in .env file')

    def _collect_games(self,data:dict):
        games = []
        for d in data['response']['games']:
            game = Game(d)
            games.append(game)
            break
        self.games = games

    def run(self):
        res = get_user_vault(steam_id = self.id,key = self.api_key)
        self._collect_games(res)
        print(self.games[0].__str__())
if __name__ == '__main__':
    user = User()
    user.run()