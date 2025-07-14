import requests

VAULT_BASE = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001'
INFO_BASE = 'https://store.steampowered.com/api/appdetails?appids='

def get_user_vault(steam_id:str, key:str):
    uri = VAULT_BASE + '?key=' + key + '&steamid='+ steam_id + '&include_appinfo=true&format=json'
    headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78'
    }
    response = requests.get(uri,headers=headers)
    if response.status_code != 200:
        raise Exception('Failed to get vault')
    return response.json()

def get_game_info(app_id:str):
    uri = INFO_BASE + app_id
    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78'
        }
    response = requests.get(uri,headers=headers)
    if response.status_code != 200:
        raise Exception('Failed to get game info')
    return response.json()[app_id]