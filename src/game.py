import re
import time
from datetime import datetime
from api import get_game_info
from utils import filter_invailed_genres


class Game:
    def __init__(self, data:dict):
        self.game_id: int = data['appid']
        self.name = data['name']
        self.playtime = data['playtime_forever']
        self.last_played_timestamp = data.get('rtime_last_played')

    def format_last_played(self):
        """将时间戳转换为可读的时间格式"""
        if not self.last_played_timestamp:
            return "从未游玩"
        try:
            dt = datetime.fromtimestamp(self.last_played_timestamp)
            return dt.strftime("%Y年%m月%d日 %H:%M")
        except (ValueError, OSError):
            return f"无效时间戳: {self.last_played_timestamp}"
    
    def __str__(self):
        """获取分隔线内的游戏信息内容"""
        return f'''---
GameID: {self.game_id}
PlayedHours: {self.playtime/60 :.1f}
Genres: {self.genres}
Platforms: {self.platforms}
LastPlayed: {self.format_last_played()}
Cover: {self.cover}
Description: {self.description}
---'''
    

    def fetch_more_info(self):
        res = get_game_info(str(self.game_id))
        if not res['success']:
            raise Exception(f'Failed to fetch info for game {self.name} ({self.game_id})')
        data = res['data']
        self.name = data['name']
        self.platforms = []
        for key in data['platforms']:
            if data['platforms'][key]:
                self.platforms.append(key)
        genres = [d['description'] for d in data['genres']]
        self.genres = filter_invailed_genres(genres)
        self.cover = data['header_image']
        clean = re.compile('<.*?>')
        self.description = re.sub(clean,'',data['short_description'])
        self.description = self.description.replace(':','：')
        

