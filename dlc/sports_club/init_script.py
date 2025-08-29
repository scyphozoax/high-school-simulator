#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
体育俱乐部DLC初始化脚本
"""

def init_dlc(game, dlc_manager):

    print("\n[DLC] 体育俱乐部DLC 已加载~")
    
    # 添加新的常规行动：体育训练
    sports_training_action = {
        'name': '体育训练',
        'cost': 7,
        'desc': '体能 ＋4，压力值 －6，有机会提升社交',
        'type': 'exercise'
    }
    dlc_manager.register_action(sports_training_action, 'normal')
    
    # 添加新的假期行动：户外拓展
    outdoor_activity_action = {
        'name': '户外拓展',
        'cost': 5,
        'desc': '体能 ＋3，社交 ＋2，压力值 －8',
        'type': 'social'
    }
    dlc_manager.register_action(outdoor_activity_action, 'vacation')
    
    # 添加新的随机事件：体育比赛
    sports_competition_event = {
        'condition': lambda stats: stats['体能'] >= 60,
        'prob': 0.15,
        'desc': '学校举行体育比赛，你积极参与并取得了好成绩！',
        'effect': lambda stats: (
            stats.update({'体能': stats['体能'] + 3}),
            stats.update({'社交': stats['社交'] + 2}),
            stats.update({'压力值': max(0, stats['压力值'] - 5)})
        )
    }
    dlc_manager.register_event(sports_competition_event, 'random')
    
    # 添加新的固定事件：校运会
    sports_meet_event = {
        'month': 10,
        'week': 3,
        'desc': '校运会举行，你参加了多个项目，增强了体质和团队精神。',
        'effect': 'none'
    }
    dlc_manager.register_event(sports_meet_event, 'fixed')

# 当脚本被执行时自动调用init_dlc函数
if __name__ == '__main__':
    # 注意：这个条件在DLC加载时不会触发，因为脚本是被导入执行的
    pass
else:
    # 获取游戏实例和DLC管理器实例
    game = locals().get('game')
    dlc_manager = locals().get('dlc_manager')
    
    if game and dlc_manager:
        init_dlc(game, dlc_manager)
    else:
        print("[DLC] 体育俱乐部DLC 加载失败：无法获取游戏实例或DLC管理器实例。")