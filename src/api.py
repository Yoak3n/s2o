import requests
import time
from typing import Optional

VAULT_BASE = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001'
INFO_BASE = 'https://store.steampowered.com/api/appdetails?appids='

def make_request_with_retry(url: str, headers: dict, max_retries: int = 5, retry_delay: float = 1.0) -> Optional[requests.Response]:
    """带重试机制的网络请求函数"""
    retry_status_codes = {403, 429, 500, 502, 503, 504}  # 需要重试的状态码
    
    for attempt in range(max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200 or response.status_code not in retry_status_codes:
                return response
            
            if attempt < max_retries:
                wait_time = retry_delay * (2 ** attempt) 
                print(f'Request failed with status {response.status_code}, retrying in {wait_time:.1f}s... (attempt {attempt + 1}/{max_retries})')
                time.sleep(wait_time)
            else:
                return response
                
        except requests.exceptions.RequestException as e:
            if attempt < max_retries:
                wait_time = retry_delay * (2 ** attempt)
                time.sleep(wait_time)
            else:
                raise Exception(f'Network request failed after {max_retries} retries: {e}')
    
    return None

def get_user_vault(steam_id:str, key:str):
    uri = VAULT_BASE + '?key=' + key + '&steamid='+ steam_id + '&include_appinfo=true&format=json'
    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0'
    }
    
    response = make_request_with_retry(uri, headers)
    if response is None or response.status_code != 200:
        raise Exception(f'Failed to get vault: {response.status_code if response else "No response"}')
    return response.json()

def get_game_info(app_id:str):
    uri = INFO_BASE + app_id
    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0'
    }
    
    response = make_request_with_retry(uri, headers)
    if response is None or response.status_code != 200:
        raise Exception(f'Failed to get game info for {app_id}: {response.status_code if response else "No response"}')
    return response.json()[app_id]