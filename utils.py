import os

invailed_genres = ['免费开玩', '线上玩家对战', 'Steam 成就', '视角舒适度', '可选颜色', '自定义音量控制', '可调整难度',
                   '完全支持控制器', 'Steam 集换式卡牌', '支持字幕', 'Steam 创意工坊', '无需应对快速反应事件', '立体声', '环绕声', 'Steam 云',
                   '已启用 Valve 反作弊保护', '统计数据', '包括 Source SDK', '解说可用', '在手机上远程畅玩', '在平板上远程畅玩','在电视上远程畅玩',
                   '家庭共享', 'Steam 时间轴', '可以仅用鼠标','随时保存','抢先体验'
]

def filter_invailed_genres(genres:list):
    return [genre for genre in genres if genre not in invailed_genres]

def sanitize_filename(filename:str) -> str:
    char_replacements = {
        ':': '：',    
        '<': '＜',    
        '>': '＞',    
        '"': '"',    
        '|': '｜',    
        '?': '？',    
        '*': '＊',    
        '\\': '＼',   
        '/': '／'     
    }
    
    # 逐个替换非法字符
    for illegal_char, replacement in char_replacements.items():
        filename = filename.replace(illegal_char, replacement)
    
    filename = filename.strip(' .')

    if not filename:
        filename = 'unnamed_game'
    return filename

def read_existing_content(file_path: str) -> tuple[str, str]:
    """读取现有文件内容，返回分隔线前后的内容"""
    if not os.path.exists(file_path):
        return '', ''
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        first_separator = -1
        last_separator = -1
        
        for i, line in enumerate(lines):
            if line.strip() == '---':
                if first_separator == -1:
                    first_separator = i
                else:
                    last_separator = i
        
        if first_separator == -1 or last_separator == -1 or first_separator == last_separator:
            return '', ''
        # 一般情况下，第一个分隔线之前不应该存在内容,会破坏md文件的元数据
        before_content = '\n'.join(lines[:first_separator]).strip()
        after_content = '\n'.join(lines[last_separator + 1:]).strip()
        
        return before_content, after_content
    
    except Exception as e:
        print(f'Error reading existing content from {file_path}: {e}')
        return '', ''

def write_to_obsidian_vault(games:list, path:str):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    for g in games:
        clean_name = sanitize_filename(g.name)
        name = f'{clean_name}.md'
        p = os.path.join(path, name)
        
        # 读取现有文件的分隔线外内容
        before_content, after_content = read_existing_content(p)
        
        # 构建完整内容
        game_content = g.__str__()
        full_content = ''
        
        if before_content and before_content != '':
            full_content += before_content
        
        full_content += game_content
        
        if after_content:
            full_content += after_content
        
        try:
            with open(p, 'w', encoding='utf-8') as f:
                f.write(full_content)
                print(f'Wrote {g.name} to {p}')
        except OSError as e:
            print(f'Failed to write {g.name}: {e}')
            # 尝试使用游戏ID作为备用文件名
            backup_name = f'game_{g.game_id}.md'
            backup_path = os.path.join(path, backup_name)
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
                print(f'Wrote {g.name} to {backup_path} (using backup name)')
