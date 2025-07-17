import re
from datetime import datetime

from api import get_game_info,get_game_achievement
from utils import filter_invailed_genres


class Game:
    def __init__(self, data:dict):
        self.game_id: int = data['appid']
        self.name = data['name']
        self.playtime = data['playtime_forever']
        self.last_played_timestamp = data.get('rtime_last_played')
        self.achievement_total  = None
        self.achievement_count = None

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
        output = f'''---
GameID: {self.game_id}
Genres: {self.genres}
Platforms: {self.platforms}
PlayedHours: {self.playtime/60 :.1f}
LastPlayed: {self.format_last_played()}
Cover: {self.cover}
Description: {self.description}
---'''
        lines = output.split('\n')
        
        if self.score is not None:
            lines.insert(3, f'MetacriticScore: {self.score}')
        
        # 需要考虑Score是否已插入来确定正确的索引位置
        achievement_index = 5  
        if self.score is not None:
            achievement_index += 1  
        
        if self.achievement_count is not None:
            lines.insert(achievement_index, f'Achievements: {self.achievement_count}/{self.achievement_total}')
        
        if self.review_total is not None:
            lines.insert(achievement_index + 2, f'Reviews: {self.review_total}')
        
        return '\n'.join(lines)

    def fetch_more_info(self):
        """获取更多游戏信息"""
        res = get_game_info(str(self.game_id))
        if not res['success']:
            raise Exception(f'Failed to fetch info for game {self.name} ({self.game_id})')
        data :dict = res['data']
        # 游戏名
        self.name = data['name']
        # 平台
        self.platforms = []
        for key in data['platforms']:
            if data['platforms'][key]:
                self.platforms.append(key)
        # 类型
        genres = [d['description'] for d in data['genres']]
        self.genres = filter_invailed_genres(genres)
        # 封面
        self.cover = data['header_image']
        # 描述
        clean = re.compile('<.*?>')
        self.description = re.sub(clean,'',data['short_description']).replace(':','：')
        # 评分，可能为None
        self.score = data.get('metacritic',{}).get('score')
        # 成就总数
        self.achievement_total = data.get('achievements',{}).get('total')
        # 评价总数
        self.review_total = data.get('recommendations',{}).get('total')
        

    def fetch_achievement(self,steam_id: str,key: str):
        """获取游戏成就信息"""
        if self.achievement_total is None:
            return
        res = get_game_achievement(str(self.game_id),steam_id ,key)
        playerstats: dict = res['playerstats']
        if playerstats.get('error') == 'Requested app has no stats':
            return
        achievements:list = playerstats.get('achievements',[])
        self.achievement_count = len([a for a in achievements if a['achieved'] == 1])

