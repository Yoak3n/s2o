import re
from api import get_game_info
from utils import filter_invailed_genres


class Game:
    def __init__(self, data:dict):
        self.game_id: int = data['appid']
        self.name = data['name']
        self.playtime = data['playtime_forever']
        self.last_played_timestamp = data.get('rtime_last_played')

    def __str__(self):
        return f'''{self.name} ({self.game_id}) - {self.playtime/60 :.1f} hours played
Genres: {self.genres}
Platforms: {self.platforms}
Last played: {self.last_played_timestamp}
Cover art: {self.cover}
Description: {self.description}
        '''

    def fetch_more_info(self):
        res = get_game_info(str(self.game_id))
        if not res['success']:
            raise Exception(f'Failed to fetch info for game {self.name} ({self.game_id})')
        data = res['data']
       
        self.platforms = []
        for key in data['platforms']:
            if data['platforms'][key]:
                self.platforms.append(key)
        genres = [d['description'] for d in data['genres']]
        self.genres = filter_invailed_genres(genres)
        self.cover = data['header_image']
        clean = re.compile('<.*?>')
        self.description = re.sub(clean,'',data['detailed_description'])
        

