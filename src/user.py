import time
import os
from typing import List

from dotenv import load_dotenv
from tqdm import tqdm

from api import get_user_vault
from utils import write_to_obsidian_vault
from game import Game
class User:
    def __init__(self):
        self.id = ''
        self.api_key = ''
        self.games:List[Game] = []
        self._get_config()
    
    def _get_config(self):
        load_dotenv(verbose=True)
        self.id = os.getenv('ID')
        self.api_key = os.getenv('API_KEY')
        if not self.id or not self.api_key:
            raise Exception('ID and API_KEY must be set in .env file')

    def _collect_games(self, data:dict):
        games:List[Game] = []

        for d in data['response']['games']:
            game = Game(d)
            games.append(game)
        # 选择导入哪部分数据
        option = input(f'''{"="*40}
1. 仅游玩时间超过 200 小时的游戏（{len([g for g in games if g.playtime/60 >200 ])}个）
2. 仅游玩时间超过 500 小时的游戏（{len([g for g in games if g.playtime/60 > 500])}个）
3. 仅最近2个月游玩的游戏（{len([g for g in games if g.last_played_timestamp and g.last_played_timestamp > time.time() - 60*24*3600])}个）
4. 仅游玩过的游戏（{len([g for g in games if g.playtime > 0])}个）
5. 所有游戏（{len(games)}个）
{"="*40}
请选择导入游戏的范围（default=1）：''')
        if option not in ['1','2','3','4']:
            option = '1'
        # 筛选游戏
        self.games = []
        if option == '1':
            self.games = [g for g in games if g.playtime/60 > 200]
        elif option == '2':
            self.games = [g for g in games if g.playtime/60 > 500]
        elif option == '3':
            self.games = [g for g in games if g.last_played_timestamp and g.last_played_timestamp > time.time() - 60*24*3600]
        elif option == '4':
            self.games = [g for g in games if g.playtime > 0]
        elif option == '5':
            self.games = games

    def run(self):
        print('正在获取游戏列表...')
        res = get_user_vault(steam_id = self.id,key = self.api_key)
        self._collect_games(res)
        achievement_option = input('是否获取游戏成就信息？(y/N)')
        bar = tqdm(self.games, desc='获取游戏信息', unit='Game')
        for g in bar:
            bar.set_description(f'获取游戏 {g.name} 的详细信息')
            g.fetch_more_info()
            if achievement_option.lower() == 'y':
                bar.set_description(f'获取游戏 {g.name} 的成就信息')
                g.fetch_achievement(steam_id = self.id,key = self.api_key)
            # 防限流
            time.sleep(1)   
        bar.close()
        target = os.getenv('DIR')
        if target is None:
            raise Exception('DIR must be set in .env file')
        write_to_obsidian_vault(self.games, os.getenv('DIR'))


