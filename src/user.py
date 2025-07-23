import time
import os
from typing import List

from dotenv import load_dotenv
from tqdm import tqdm

from api import get_user_vault
from utils import sanitize_filename,read_existing_content
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
        if option not in ['1','2','3','4','5']:
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

    def __write_game_info__(self,game:Game):
        clean_name = sanitize_filename(game.name)
        name = f'{clean_name}.md'
        abs_path = os.path.join(target, name)
        before_content, after_content = read_existing_content(abs_path)

        full_content = ''
        if before_content and before_content != '':
            full_content += before_content
        
        full_content += str(game)
        if after_content and after_content != '':
            full_content += '\n' + after_content
        
        try:
            with open(abs_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
        except OSError as e:
            print(f'Failed to write {game.name}: {e}')
            backup_name = f'game_{game.game_id}.md'
            backup_path = os.path.join(target, backup_name)
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
                print(f'Wrote {game.name} to {backup_path} (using backup name)')



    def run(self):
        print('正在获取游戏列表...')
        res = get_user_vault(steam_id = self.id,key = self.api_key)
        self._collect_games(res)

        target = os.getenv('DIR')
        if target is None:
            raise Exception('DIR must be set in .env file')
        if not os.path.exists(target):
            os.makedirs(target, exist_ok=True)

        option = input('是否忽略工具或软件？(y/N)')
        achievement_option = input('是否获取游戏成就信息？(y/N)')

        bar = tqdm(self.games, desc='获取游戏信息', unit='Game')
        for g in bar:
            try:
                bar.set_description(f'获取游戏 {g.name} 的详细信息')
                g.fetch_more_info()
                if option.lower() == 'y' and ('实用工具' or 'Utilities') in g.genres:
                    continue
                if achievement_option.lower() == 'y':
                    bar.set_description(f'获取游戏 {g.name} 的成就信息')
                    g.fetch_achievement(steam_id = self.id,key = self.api_key)

                self.__write_game_info__(g)
                # 防限流
                time.sleep(1)   
            except Exception as e:
                print(f'获取游戏 {g.name} 的详细信息失败',e)
                continue
            

        bar.close()
        print('游戏信息已获取并写入文件')


