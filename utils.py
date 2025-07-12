invailed_genres = ['免费开玩', '线上玩家对战', 'Steam 成就', '视角舒适度', '可选颜色', '自定义音量控制', '可调整难度',
                   '完全支持控制器', 'Steam 集换式卡牌', '支持字幕', 'Steam 创意工坊', '无需应对快速反应事件', '立体声', '环绕声', 'Steam 云',
                   '已启用 Valve 反作弊保护', '统计数据', '包括 Source SDK', '解说可用', '在手机上远程畅玩', '在平板上远程畅玩','在电视上远程畅玩',
                   '家庭共享', 'Steam 时间轴', '可以仅用鼠标','随时保存','抢先体验'
]

def filter_invailed_genres(genres:list):
    return [genre for genre in genres if genre not in invailed_genres]