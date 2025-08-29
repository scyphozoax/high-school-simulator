#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Chinese High School Student Simulator 
            by Sanchess Syurp Praline Stollen
    Ver private_test 1010
"""
import random
import time
import os
import calendar
import json
from datetime import datetime, timedelta, date
from dlc_manager import DLCManager

# ANSI 颜色代码
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'  # 亮红
    GREEN = '\033[92m'  # 亮绿
    YELLOW = '\033[93m'  # 亮黄
    BLUE = '\033[94m'  # 亮蓝
    MAGENTA = '\033[95m'  # 亮品红
    CYAN = '\033[96m'  # 亮青
    WHITE = '\033[97m'  # 亮白
    BROWN = '\033[38;5;173m'  # 亮棕
    LIGHT_BLUE = '\033[38;5;159m'  # 更亮的蓝
    DARK_BLUE = '\033[38;5;75m'  # 替换为亮蓝
    GRAY = '\033[38;5;245m'  # 亮灰
    LIGHT_YELLOW = '\033[38;5;228m'  # 更亮的黄
    LIGHT_GREEN = '\033[38;5;120m'  # 更亮的绿
    SKY_BLUE = '\033[38;5;153m'  # 更亮的天蓝

# 导入游戏数据库


# 游戏数值设置和计算

# 初始属性设置
def get_initial_stats():
    return {
        '智力': random.randint(35, 55),
        '记忆力': random.randint(35, 55),
        '体能': random.randint(35, 55),
        '社交': random.randint(35, 55),
        '自律性': random.randint(35, 55),
        '压力值': 20,
        '体力值': 30,
        '体力上限': 30
    }

# 初始学科熟练度设置
def get_initial_subjects():
    return {
        '语文': 20,
        '数学': 20,
        '英语': 20,
        '物理': 20,
        '化学': 20,
        '生物': 20,
        '政治': 20,
        '历史': 20,
        '地理': 20
    }

# 计算属性成长
def calculate_stat_growth(base_value, growth_rate=1.0):
    # 成长难度随数值增加而增加
    if base_value < 50:
        gain = random.randint(1, 3) * growth_rate
    elif base_value < 70:
        gain = random.randint(1, 2) * growth_rate
    else:
        gain = random.randint(0, 1) * growth_rate
    return int(gain)

# 计算学科熟练度成长
def calculate_subject_growth(base_value, stats, difficulty=1.0):
    # 考虑智力和自律性对学习效果的影响
    bonus = (stats['智力'] // 20) + (stats['自律性'] // 20)
    if base_value < 50:
        gain = random.randint(3, 5) + bonus
    elif base_value < 70:
        gain = random.randint(2, 4) + bonus
    elif base_value < 90:
        gain = random.randint(1, 3) + bonus
    else:
        gain = random.randint(0, 2) + bonus
    return int(gain * difficulty)

# 计算考试成绩
def calculate_exam_score(subjects, stats, exam_type='weekly'):
    # 根据考试类型调整权重
    if exam_type == 'weekly':
        weight = 0.7
    elif exam_type == 'monthly':
        weight = 0.8
    elif exam_type == 'final':
        weight = 1.0
    else:
        weight = 0.7

    # 计算基础分数
    base_score = 0
    valid_subjects = [subj for subj in subjects if subjects[subj] != -1]
    for subj in valid_subjects:
        base_score += subjects[subj] * weight

    # 计算状态加成
    status = (stats['智力'] + stats['记忆力'] + stats['自律性']) // 3 - stats['压力值'] // 5
    status_bonus = max(0, status) // 2

    # 计算最终分数
    final_score = base_score + status_bonus
    return min(750, final_score)  # 满分750

# 计算结局
def calculate_ending(subjects, stats):
    # 计算最终成绩
    final_score = calculate_exam_score(subjects, stats, 'final')

    # 判断结局
    if final_score >= 630 and stats['自律性'] >= 70:
        return {'type': 'excellent', 'desc': '恭喜你被顶尖大学录取！你的努力得到了回报。'}
    elif final_score >= 500 and stats['自律性'] >= 50:
        return {'type': 'good', 'desc': '你被一本大学录取了！继续加油吧。'}
    elif final_score >= 400:
        return {'type': 'average', 'desc': '你被二本大学录取了。大学是新的起点，继续努力！'}
    else:
        return {'type': 'bad', 'desc': '很遗憾，你没有达到大学录取分数线。不要灰心，人生还有很多可能。'}

# 游戏剧情数据库

# 固定剧情
def get_fixed_events():
    return [
        {'month': 9, 'week': 1, 'desc': '高三开学：你怀着紧张而期待的心情踏入教室，高三一年的冲刺正式开始了。', 'effect': 'none'},
        {'month': 10, 'week': 2, 'desc': '第一次月考：高三的第一次正式考试，大家都拼尽全力。', 'effect': 'exam'},
        {'month': 11, 'week': 3, 'desc': '期中考试：半个学期过去了，高考的脚步越来越近。', 'effect': 'exam'},
        {'month': 1, 'week': 2, 'desc': '期末考试：高三上学期结束，寒假期间也要抓紧复习。', 'effect': 'exam'},
        {'month': 3, 'week': 1, 'desc': '百日誓师：距离高考仅剩100天，学校举行誓师大会鼓舞士气。', 'effect': 'none'},
        {'month': 4, 'week': 2, 'desc': '二模考试：模拟高考的重要考试，检验复习成果。', 'effect': 'exam'},
        {'month': 5, 'week': 3, 'desc': '高考冲刺：最后的复习阶段，大家都在为梦想奋力一搏。', 'effect': 'none'},
        {'month': 6, 'week': 1, 'desc': '高考：终于到了检验一年努力成果的时刻。', 'effect': 'exam'}
    ]

# 随机剧情
def get_random_events():
    return [
        {'condition': lambda stats: stats['自律性'] >= 70, 'prob': 0.2,
         'desc': '发现高效复习方法：你找到了适合高考冲刺的复习方法，学习效率大幅提升。',
         'effect': lambda stats: stats.update({'智力': stats['智力'] + 2})},
        {'condition': lambda stats: stats['社交'] >= 60, 'prob': 0.3,
         'desc': '小组学习：和同学组成学习小组，互相帮助，共同进步。',
         'effect': lambda stats, subjects: (stats.update({'自律性': stats['自律性'] + 1}),
                                           subjects.update({list(subjects.keys())[0]: subjects[list(subjects.keys())[0]] + 3}) )},
        {'condition': lambda stats: stats['自律性'] <= 40, 'prob': 0.4,
         'desc': '复习分心：学习时注意力不集中，浪费了宝贵的复习时间。',
         'effect': lambda stats, _: stats.update({'自律性': max(0, stats['自律性'] - 1)})},
        {'condition': lambda stats: stats['体能'] >= 60, 'prob': 0.2,
         'desc': '课间运动：短暂的运动让你精神焕发，压力也减轻了不少。',
         'effect': lambda stats: (stats.update({'体能': stats['体能'] + 2}),
                                 stats.update({'压力值': max(0, stats['压力值'] - 3)}))},
        {'condition': lambda stats: stats['压力值'] >= 70, 'prob': 0.3,
         'desc': '压力过大：长期高压状态影响了身心健康，学习效率下降。',
         'effect': lambda stats: (stats.update({'智力': max(0, stats['智力'] - 1)}),
                                 stats.update({'体能': max(0, stats['体能'] - 1)}))},
        {'condition': lambda stats: stats['记忆力'] >= 80, 'prob': 0.2,
         'desc': '记忆爆发：突然想起了很多知识点，学习效果显著。',
         'effect': lambda stats, subjects: subjects.update({list(subjects.keys())[0]: subjects[list(subjects.keys())[0]] + 5})}
    ]

class HighSchoolSimulator:
    def clear_screen(self):
        """清屏函数"""
        # 根据设置决定是否清屏
        if not self.game_state.get('disable_screen_clear', False):
            # 根据操作系统执行不同的清屏命令
            os.system('cls' if os.name == 'nt' else 'clear')
        
    def to_full_width(self, text):
        """将半角数字转换为全角数字"""
        full_width_chars = {'0': '０', '1': '１', '2': '２', '3': '３', '4': '４', '5': '５', '6': '６', '7': '７', '8': '８', '9': '９'}
        return ''.join([full_width_chars.get(char, char) for char in str(text)])
    def __init__(self):
        """初始化游戏状态"""
        # 角色属性 - 获取初始属性
        self.stats = get_initial_stats()
        
        # 学科熟练度 - 获取初始熟练度
        self.subjects = get_initial_subjects()
        
        # 游戏状态
        self.game_state = {
            'current_date': datetime(2024, 9, 2),  # 开始日期: 2024年9月2日
            'current_day': datetime(2024, 9, 2).weekday() + 1,  # 1-7, 周一=1, 周日=7

            'science_arts': 'science',  # 高三默认已分科，这里设置为理科
            'last_study': {subj: 0 for subj in self.subjects},  # 记录上次学习各科目天数
            'last_social': 0,       # 记录上次社交活动天数
            'last_exercise': 0,     # 记录上次运动天数
            'exam_rank': {'weekly': 50, 'monthly': 500},  # 考试排名
            'game_over': False,
            'ending': None,
            'rest_weeks': 0,  # 用于跟踪双周休息
            'disable_screen_clear': False  # 是否禁用屏幕刷新
        }

        # 初始化DLC管理器
        self.dlc_manager = DLCManager(self)
        
        # 常规行动列表
        self.normal_actions = [
            {'name': '早自习刷题', 'cost': 8, 'desc': '对应科目熟练度 ＋３～５，自律性 ＋１', 'type': 'study'},
            {'name': '专题突破', 'cost': 10, 'desc': '目标科目熟练度 ＋６～８，压力值 ＋３', 'type': 'study'},
            {'name': '晚自习复盘', 'cost': 7, 'desc': '本周学习效果固化１０％，记忆力 ＋１', 'type': 'study'},
            {'name': '操场跑步', 'cost': 5, 'desc': '体能 ＋２，压力值 －５', 'type': 'exercise'},
            {'name': '与同学讨论', 'cost': 4, 'desc': '社交 ＋１，随机科目熟练度 ＋２', 'type': 'social'},

            {'name': '休息', 'cost': 0, 'desc': '体力值 ＋５，压力值 －８', 'type': 'rest'}
        ]
        
        # 假期行动列表
        self.vacation_actions = [
            {'name': '自主学习', 'cost': 6, 'desc': '自选科目熟练度 ＋４～６，自律性 ＋２', 'type': 'study'},
            {'name': '图书馆阅读', 'cost': 4, 'desc': '随机科目熟练度 ＋３～５，智力 ＋１', 'type': 'study'},
            {'name': '户外锻炼', 'cost': 3, 'desc': '体能 ＋３，压力值 －６', 'type': 'exercise'},
            {'name': '走亲访友', 'cost': 2, 'desc': '社交 ＋２，压力值 －４', 'type': 'social'},
            {'name': '家务劳动', 'cost': 5, 'desc': '体能 ＋１，自律性 ＋２', 'type': 'exercise'},
            {'name': '线上学习', 'cost': 7, 'desc': '对应科目熟练度 ＋５～７，压力值 ＋２', 'type': 'study'},
            {'name': '彻底放松', 'cost': 0, 'desc': '体力值 ＋８，压力值 －１０', 'type': 'rest'}
        ]
        
        # 根据当前状态选择行动列表
        self.actions = self.normal_actions.copy()
        
        # 剧情事件库
        self.events = {
            'fixed': get_fixed_events(),
            'random': get_random_events()
        }

    def print_status(self):
        """打印当前游戏状态"""
        self.clear_screen()
        print(f"\n{Colors.LIGHT_YELLOW}====== 状态 ======{Colors.RESET}")
        # 格式化日期显示（数字全角）
        year = self.to_full_width(self.game_state['current_date'].year)
        month = self.to_full_width(self.game_state['current_date'].month)
        day = self.to_full_width(self.game_state['current_date'].day)
        date_str = f'{year}年{month}月{day}日'
        weekday_str = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][self.game_state['current_date'].weekday()]
        print(f"{Colors.CYAN}日期:{Colors.RESET} {date_str} {weekday_str}")
        
        # 计算距离高考的剩余天数
        college_entrance_exam_date = datetime(2025, 6, 7)
        remaining_days = (college_entrance_exam_date - self.game_state['current_date']).days
        # 确保剩余天数不为负数
        remaining_days = max(0, remaining_days)
        print(f"{Colors.RED}距离高考还剩:{Colors.RESET} {self.to_full_width(remaining_days)} 天")
        
        # 检查是否为假期
        is_vacation = self.is_vacation()
        if is_vacation:
            print(f"{Colors.YELLOW}状态:{Colors.RESET} 假期")
        else:
            # 检查是否为休息日
            is_rest_day = self.is_rest_day()
            if is_rest_day:
                print(f"{Colors.GREEN}状态:{Colors.RESET} 休息日")
            else:
                print(f"{Colors.CYAN}状态:{Colors.RESET} 学习日")

        print("\n------ 属性 ------")
        
        # 属性颜色映射
        stat_colors = {
            '智力': Colors.BLUE,
            '记忆力': Colors.MAGENTA,
            '体能': Colors.GREEN,
            '社交': Colors.YELLOW,
            '自律性': Colors.CYAN,
            '压力值': Colors.RED,
            '体力值': Colors.LIGHT_GREEN,
        }
        
        for stat, value in self.stats.items():
            if stat == '体力上限':
                continue
            color = stat_colors.get(stat, Colors.WHITE)
            if stat in ['体力值', '压力值']:
                # 为体力和压力创建可视化进度条
                if stat == '压力值':
                    max_value = 100  # 压力值上限固定为100
                else:  # 体力值
                    max_value = self.stats['体力上限']  # 使用当前体力上限
                bar_length = 20
                filled_length = int(bar_length * value / max_value)
                bar = '█' * filled_length + '░' * (bar_length - filled_length)
                # 为体力值和压力值设置不同的警告阈值
                warning = ''
                if stat == '体力值' and value < max_value * 0.3:
                    warning = f"{Colors.RED}注意! 体力不足{Colors.RESET}"
                elif stat == '压力值' and value > 70:
                    warning = f"{Colors.RED}注意! 压力过大{Colors.RESET}"
                print(f"{color}{stat}: {self.to_full_width(value)}/{self.to_full_width(max_value)} |{bar}| {Colors.RESET}{warning}")
            else:
                print(f"{color}{stat}: {self.to_full_width(value)}{Colors.RESET}")
        print("\n----- 学科熟练度 -----")
        
        # 学科颜色映射
        subject_colors = {
            '语文': Colors.BROWN,
            '数学': Colors.BLUE,
            '英语': Colors.SKY_BLUE,
            '物理': Colors.DARK_BLUE,
            '化学': Colors.MAGENTA,
            '生物': Colors.LIGHT_GREEN,
            '政治': Colors.RED,
            '历史': Colors.BROWN,
            '地理': Colors.CYAN
        }
        
        # 只显示所选科目的熟练度
        if self.game_state['science_arts'] == 'science':
            subjects = ['语文', '数学', '英语', '物理', '化学', '生物']
        elif self.game_state['science_arts'] == 'arts':
            subjects = ['语文', '数学', '英语', '政治', '历史', '地理']
        else:
            subjects = list(self.subjects.keys())
        for subj in subjects:
            color = subject_colors.get(subj, Colors.WHITE)
            print(f"{color}{subj}: {self.to_full_width(self.subjects[subj])}{Colors.RESET}")
        print(f"{Colors.LIGHT_YELLOW}===================={Colors.RESET}\n")

    def check_events(self):
        """检查并触发事件"""
        # 检查固定事件
        current_month = self.game_state['current_date'].month
        # 计算当月的周数（简单计算，假设每月4周）
        current_week_in_month = (self.game_state['current_date'].day - 1) // 7 + 1
        
        for event in self.events['fixed']:
            if event['month'] == current_month and event['week'] == current_week_in_month:
                print(f"\n[事件] {event['desc']}")
                if event['effect'] == 'exam':
                    # 根据月份和周数决定考试类型
                    if current_month in [1, 6]:  # 1月和6月有期末考试
                        self.take_exam('final')
                    elif current_month in [10, 4]:  # 10月和4月有月考/二模
                        self.take_exam('monthly')
                    else:  # 其他考试
                        self.take_exam('weekly')
                elif event['effect'] == 'holiday':
                    self.holiday_effect()
                elif event['effect'] == 'divide':
                    # 高三默认已分科，这里可以改为调整科目权重或提供复习建议
                    print("高三已分科，你可以根据自己的选择专注复习相应科目。")
                elif event['effect'] == 'none':
                    pass  # 无特殊效果
                # 移除已触发的固定事件
                self.events['fixed'].remove(event)
                break
        
        # 检查随机事件
        for event in self.events['random']:
            if event['condition'](self.stats) and random.random() < event['prob']:
                print(f"\n[随机事件] {event['desc']}")
                if callable(event['effect']):
                    event['effect'](self.stats, self.subjects)
                break

    def choose_science_arts(self):
        """选择文理分科"""
        print(f"\n{Colors.LIGHT_YELLOW}===== 文理分科 ====={Colors.RESET}")
        print(f"{Colors.CYAN}{self.to_full_width(1)}{Colors.RESET}. {Colors.BLUE}理科{Colors.RESET} (物理、化学、生物)")
        print(f"{Colors.CYAN}{self.to_full_width(2)}{Colors.RESET}. {Colors.RED}文科{Colors.RESET} (政治、历史、地理)")
        choice = input(f"请选择分科方向 ({Colors.CYAN}{self.to_full_width(1)}{Colors.RESET}/{Colors.CYAN}{self.to_full_width(2)}{Colors.RESET}): ")
        while choice not in ['1', '2']:
            choice = input(f"输入无效，请重新选择 ({Colors.CYAN}{self.to_full_width(1)}{Colors.RESET}/{Colors.CYAN}{self.to_full_width(2)}{Colors.RESET}): ")
        
        self.game_state['science_arts'] = 'science' if choice == '1' else 'arts'
        print(f"{Colors.GREEN}你选择了{'理科' if choice == '1' else '文科'}，今后将重点学习对应的科目。{Colors.RESET}")
        
        # 非所选科目的熟练度停止增长
        if self.game_state['science_arts'] == 'science':
            stop_subjects = ['政治', '历史', '地理']
        else:
            stop_subjects = ['物理', '化学', '生物']
        for subj in stop_subjects:
            self.subjects[subj] = -1  # 标记为不再增长
        print(f"{Colors.LIGHT_YELLOW}===================={Colors.RESET}\n")

    def take_action(self, action_idx):
        """执行选择的行动"""
        action = self.actions[action_idx]
        
        # 检查体力是否足够
        if self.stats['体力值'] < action['cost']:
            print("体力不足，无法执行此行动。")
            return False
        
        # 扣除体力
        self.stats['体力值'] -= action['cost']

        
        print(f"\n你执行了 '{action['name']}' 行动。")
        print(f"效果: {action['desc']}")
        
        # 执行行动效果
        if action['name'] == '早自习刷题':
            # 选择科目
            if self.game_state['science_arts'] == 'science':
                subjects = ['语文', '数学', '英语', '物理', '化学', '生物']
            elif self.game_state['science_arts'] == 'arts':
                subjects = ['语文', '数学', '英语', '政治', '历史', '地理']
            else:
                subjects = list(self.subjects.keys())
            
            print("可选择的科目:")
            for i, subj in enumerate(subjects):
                if self.subjects[subj] != -1:  # 未被停止的科目
                    print(f"{i+1}. {subj}")
            
            choice = int(input("请选择刷题科目: ")) - 1
            while choice < 0 or choice >= len(subjects) or self.subjects[subjects[choice]] == -1:
                choice = int(input("输入无效，请重新选择: ")) - 1
            
            subj = subjects[choice]
            base = random.randint(3, 5)
            bonus = 0
            if subj in ['语文', '英语', '政治', '历史', '地理'] and self.game_state['science_arts'] == 'arts':
                bonus = self.stats['记忆力'] // 20
            
            gain = base + bonus
            # 熟练度上限控制
            cap = self.get_subject_cap(subj)
            if self.subjects[subj] + gain > cap:
                gain = cap - self.subjects[subj]
                print(f"{Colors.YELLOW}{subj} 熟练度已达到上限，本次只增加 {self.to_full_width(gain)}{Colors.RESET}")
            self.subjects[subj] += gain
            self.stats['自律性'] += 1
            print(f"{Colors.GREEN}{subj} 熟练度 ＋{self.to_full_width(gain)}，自律性 ＋{self.to_full_width(1)}{Colors.RESET}")
            
        elif action['name'] == '专题突破':
            # 选择科目
            if self.game_state['science_arts'] == 'science':
                subjects = ['语文', '数学', '英语', '物理', '化学', '生物']
            elif self.game_state['science_arts'] == 'arts':
                subjects = ['语文', '数学', '英语', '政治', '历史', '地理']
            else:
                subjects = list(self.subjects.keys())
            
            print("可选择的科目:")
            for i, subj in enumerate(subjects):
                if self.subjects[subj] != -1:  # 未被停止的科目
                    print(f"{i+1}. {subj}")
            
            choice = int(input("请选择突破科目: ")) - 1
            while choice < 0 or choice >= len(subjects) or self.subjects[subjects[choice]] == -1:
                choice = int(input("输入无效，请重新选择: ")) - 1
            
            subj = subjects[choice]
            base = random.randint(6, 8)
            bonus1 = self.stats['智力'] // 8
            bonus2 = self.stats['自律性'] // 10
            bonus3 = 0
            if subj in ['数学', '物理', '化学', '生物'] and self.game_state['science_arts'] == 'science':
                bonus3 = self.stats['智力'] // 20
            
            gain = base + bonus1 + bonus2 + bonus3
            # 熟练度上限控制
            cap = self.get_subject_cap(subj)
            if self.subjects[subj] + gain > cap:
                gain = cap - self.subjects[subj]
                print(f"{Colors.YELLOW}{subj} 熟练度已达到上限，本次只增加 {self.to_full_width(gain)}{Colors.RESET}")
            self.subjects[subj] += gain
            self.stats['压力值'] += 3
            print(f"{Colors.GREEN}{subj} 熟练度 ＋{self.to_full_width(gain)}{Colors.RESET}，{Colors.RED}压力值 ＋{self.to_full_width(3)}{Colors.RESET}")
            
        elif action['name'] == '晚自习复盘':
            # 记忆力上限控制
            if self.stats['记忆力'] < 100:
                self.stats['记忆力'] += 1
                print(f"{Colors.GREEN}记忆力 ＋1{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}记忆力已达到上限，无法继续增加{Colors.RESET}")
            # 固化本周学习效果
            try:
                for subj in list(self.subjects.keys()):  # 使用list()确保遍历过程中字典不会被修改
                    if isinstance(self.subjects[subj], int) and self.subjects[subj] != -1:
                        new_value = int(self.subjects[subj] * 1.1)
                        cap = self.get_subject_cap(subj)
                        if new_value > cap:
                            gain = cap - self.subjects[subj]
                            print(f"{Colors.LIGHT_YELLOW}{subj} 熟练度已接近上限，本次只固化 {self.to_full_width(gain)}{Colors.RESET}")
                            self.subjects[subj] = cap
                        else:
                            gain = new_value - self.subjects[subj]
                            self.subjects[subj] = new_value
                            print(f"{Colors.GREEN}{subj} 熟练度 ＋{self.to_full_width(gain)} (固化10%){Colors.RESET}")
                    elif self.subjects[subj] == -1:
                        # 跳过标记为不再增长的科目
                        pass
                    else:
                        print(f"{Colors.RED}警告: {subj} 的熟练度值类型异常: {type(self.subjects[subj])}，已跳过{Colors.RESET}")
                print(f"{Colors.GREEN}所有有效科目熟练度已固化10%{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}晚自习复盘过程中发生错误: {str(e)}{Colors.RESET}")
            
        elif action['name'] == '操场跑步':
            # 体能提升值 = 基础加成(2) + 随机波动(±1)
            gain = 2 + random.randint(-1, 1)
            # 体能上限控制
            if self.stats['体能'] + gain > 100:
                gain = 100 - self.stats['体能']
                print(f"{Colors.YELLOW}体能已达到上限，本次只增加 {self.to_full_width(gain)}{Colors.RESET}")
            self.stats['体能'] += gain
            self.stats['压力值'] = max(0, self.stats['压力值'] - 5)
            print(f"{Colors.GREEN}体能 ＋{self.to_full_width(gain)}{Colors.RESET}，{Colors.GREEN}压力值 －{self.to_full_width(5)}{Colors.RESET}")
            
        elif action['name'] == '与同学讨论':
            # 社交上限控制
            if self.stats['社交'] < 100:
                self.stats['社交'] += 1
            else:
                print(f"{Colors.YELLOW}社交已达到上限，无法继续增加{Colors.RESET}")
            # 随机科目熟练度 +2
            if self.game_state['science_arts'] == 'science':
                subjects = ['语文', '数学', '英语', '物理', '化学', '生物']
            elif self.game_state['science_arts'] == 'arts':
                subjects = ['语文', '数学', '英语', '政治', '历史', '地理']
            else:
                subjects = list(self.subjects.keys())
            
            subj = random.choice(subjects)
            while self.subjects[subj] == -1:
                subj = random.choice(subjects)
            
            # 熟练度上限控制
            cap = self.get_subject_cap(subj)
            if self.subjects[subj] + 2 > cap:
                gain = cap - self.subjects[subj]
                print(f"{Colors.YELLOW}{subj} 熟练度已达到上限，本次只增加 {self.to_full_width(gain)}{Colors.RESET}")
                self.subjects[subj] = cap
            else:
                self.subjects[subj] += 2
            print(f"{Colors.GREEN}社交 ＋{self.to_full_width(1)}{Colors.RESET}，{Colors.GREEN}{subj} 熟练度 ＋{self.to_full_width(2)}{Colors.RESET}")
            
        elif action['name'] == '周末补课':
            # 选择薄弱科目
            if self.game_state['science_arts'] == 'science':
                subjects = ['语文', '数学', '英语', '物理', '化学', '生物']
            elif self.game_state['science_arts'] == 'arts':
                subjects = ['语文', '数学', '英语', '政治', '历史', '地理']
            else:
                subjects = list(self.subjects.keys())
            
            # 筛选出非-1的科目
            valid_subjects = [subj for subj in subjects if self.subjects[subj] != -1]
            # 找到熟练度最低的科目
            weakest_subj = min(valid_subjects, key=lambda x: self.subjects[x])
            
            # 熟练度上限控制
            cap = self.get_subject_cap(weakest_subj)
            if self.subjects[weakest_subj] + 8 > cap:
                gain = cap - self.subjects[weakest_subj]
                print(f"{Colors.YELLOW}{weakest_subj} 熟练度已达到上限，本次只增加 {self.to_full_width(gain)}{Colors.RESET}")
                self.subjects[weakest_subj] = cap
            else:
                self.subjects[weakest_subj] += 8
            self.stats['体力上限'] -= 2
            print(f"{Colors.GREEN}{weakest_subj} 熟练度 ＋{self.to_full_width(8)}{Colors.RESET}")
            
        elif action['name'] == '休息':
            # 恢复体力 = 基础恢复(6) + 体能/15 (降低恢复速度)
            gain = 6 + self.stats['体能'] // 15
            self.stats['体力值'] = min(self.stats['体力上限'], self.stats['体力值'] + gain)
            self.stats['压力值'] = max(0, self.stats['压力值'] - 6)
            print(f"{Colors.GREEN}体力值 ＋{self.to_full_width(gain)}{Colors.RESET}，{Colors.GREEN}压力值 －{self.to_full_width(6)}{Colors.RESET}")
        
        # 行动完成后自动推进到下一天
        self.next_day()
        return True

    def get_subject_cap(self, subject):
        """获取科目熟练度上限
           语数英上限为120，其他科目为100"""
        if subject in ['语文', '数学', '英语']:
            return 120
        else:
            return 100
            
    def get_rating(self, score):
        """根据分数获取评级 (D~A+)"""
        if score >= 90:
            return 'A+'
        elif score >= 75:
            return 'A'
        elif score >= 60:
            return 'B'
        elif score >= 40:
            return 'C'
        else:
            return 'D'
            
    def take_exam(self, exam_type):
        """进行考试"""
        if exam_type.startswith('monthly'):
            exam_name = '月考' + ('（第一天）' if exam_type == 'monthly_day1' else '（第二天）')
        elif exam_type.startswith('final'):
            exam_name = '期末考试' + ('（第一天）' if exam_type == 'final_day1' else '（第二天）')
        else:
            exam_name = '周测'
        print(f"\n{Colors.LIGHT_YELLOW}===== {exam_name} ====={Colors.RESET}")
        
        # 科目颜色映射
        subject_colors = {
            '语文': Colors.BROWN,
            '数学': Colors.BLUE,
            '英语': Colors.GREEN,
            '物理': Colors.DARK_BLUE,
            '化学': Colors.RED,
            '生物': Colors.LIGHT_GREEN,
            '政治': Colors.RED,
            '历史': Colors.BROWN,
            '地理': Colors.CYAN
        }
        
        if exam_type == 'weekly':
            # 周测只考一门科目
            if self.game_state['science_arts'] == 'science':
                subjects = ['语文', '数学', '英语', '物理', '化学', '生物']
            elif self.game_state['science_arts'] == 'arts':
                subjects = ['语文', '数学', '英语', '政治', '历史', '地理']
            else:
                subjects = list(self.subjects.keys())
            
            # 随机选择一门科目
            subj = random.choice(subjects)
            # 周测考所有科目
            total_score = 0
            avg_score = 0
            valid_subjects = 0
            subject_scores = {}

            print(f"{Colors.LIGHT_YELLOW}各科成绩:{Colors.RESET}")
            for subject in self.subjects:
                if self.subjects[subject] != -1:
                    valid_subjects += 1
                    proficiency = self.subjects[subject]
                    status = (self.stats['自律性'] + self.stats['智力'] // 2) // 2
                    random_bonus = random.randint(1, 3)
                    # 语数英熟练度上限提高，调整计算系数以平衡分数
                    if subject in ['语文', '数学', '英语']:
                        score = int(proficiency * 0.6 + status * 0.3 + random_bonus)
                    else:
                        score = int(proficiency * 0.7 + status * 0.2 + random_bonus)
                    subject_scores[subject] = score

                    # 成绩颜色
                    score_color = Colors.GREEN if score >= 80 else Colors.BLUE if score >= 60 else Colors.RED
                    # 获取评级
                    rating = self.get_rating(score)
                    rating_color = Colors.GREEN if rating in ['A', 'A+'] else Colors.BLUE if rating == 'B' else Colors.YELLOW if rating == 'C' else Colors.RED
                    time.sleep(0.5)
                    print(f"{subject_colors[subject]}{subject}{Colors.RESET}: {score_color}{self.to_full_width(score)}{Colors.RESET} [{rating_color}{rating}{Colors.RESET}]")

            # 计算总分和平均分
            if valid_subjects > 0:
                total_score = sum(subject_scores.values())
                avg_score = total_score / valid_subjects

            # 总分和平均分颜色
            total_color = Colors.GREEN if avg_score >= 80 else Colors.BLUE if avg_score >= 60 else Colors.RED

            time.sleep(0.5)
            print(f"总分: {total_color}{self.to_full_width(total_score)}{Colors.RESET}")
            time.sleep(0.5)
            print(f"平均分: {total_color}{self.to_full_width(f'{avg_score:.1f}')}{Colors.RESET}")

            # 计算排名 (模拟其他学生成绩)
            max_avg = min(100, avg_score + 10)
            other_avgs = [random.randint(30, int(max_avg)) for _ in range(49)]
            all_avgs = other_avgs + [avg_score]
            all_avgs.sort(reverse=True)
            rank = all_avgs.index(avg_score) + 1

            self.game_state['exam_rank']['weekly'] = rank

            # 排名颜色
            rank_color = Colors.GREEN if rank <= 10 else Colors.BLUE if rank <= 30 else Colors.RED

            print(f"班级排名: {rank_color}{self.to_full_width(rank)}{Colors.RESET}/{self.to_full_width(50)}")

            # 成绩影响
            if rank <= 10:
                print(f"{Colors.GREEN}恭喜！你获得了'免作业卡'，1次行动可替换为自由活动。{Colors.RESET}")
            elif rank >= 46:
                print(f"{Colors.RED}老师单独辅导：强制消耗1次晚自习，所有科目熟练度 +3。{Colors.RESET}")
                for subj in self.subjects:
                    if self.subjects[subj] != -1:
                        self.subjects[subj] += 3
        
        elif exam_type.startswith('monthly'):  # 月考
            # 初始化月考分数存储
            if 'monthly_exam_scores' not in self.game_state:
                self.game_state['monthly_exam_scores'] = {}
                self.game_state['monthly_total_score'] = 0
                self.game_state['monthly_exam_complete'] = False
            
            # 确定考试科目
            if exam_type == 'monthly_day1':
                # 第一天考语数英
                exam_subjects = ['语文', '数学', '英语']
                weights = {'语文': 1.2, '数学': 1.2, '英语': 1.2}
            else:  # monthly_day2
                # 第二天考其他科目
                if self.game_state['science_arts'] == 'science':
                    exam_subjects = ['物理', '化学', '生物']
                elif self.game_state['science_arts'] == 'arts':
                    exam_subjects = ['政治', '历史', '地理']
                else:
                    # 未分科时考物化生政史地中的随机3科
                    all_subjects = ['物理', '化学', '生物', '政治', '历史', '地理']
                    exam_subjects = random.sample(all_subjects, 3)
                weights = {subj: 1.0 for subj in exam_subjects}
            
            total_score = 0
            print(f"{Colors.LIGHT_YELLOW}各科成绩:{Colors.RESET}")
            for subj in exam_subjects:
                if self.subjects[subj] != -1:
                    proficiency = self.subjects[subj]
                    status = (self.stats['自律性'] + self.stats['智力'] // 2) // 2
                    random_bonus = random.randint(1, 3)
                    # 语数英熟练度上限提高，调整计算系数以平衡分数
                    if subj in ['语文', '数学', '英语']:
                        score = int(proficiency * 0.6 + status * 0.3 + random_bonus)
                    else:
                        score = int(proficiency * 0.7 + status * 0.2 + random_bonus)
                    
                    # 成绩颜色
                    score_color = Colors.GREEN if score >= 80 else Colors.BLUE if score >= 60 else Colors.RED
                    
                    # 应用权重
                    weight = weights.get(subj, 1.0)
                    weighted_score = score * weight
                    total_score += weighted_score
                    
                    # 存储成绩
                    self.game_state['monthly_exam_scores'][subj] = {
                        'score': score,
                        'weight': weight,
                        'weighted_score': weighted_score
                    }
                    
                    # 获取评级
                    rating = self.get_rating(score)
                    rating_color = Colors.GREEN if rating in ['A', 'A+'] else Colors.BLUE if rating == 'B' else Colors.YELLOW if rating == 'C' else Colors.RED
                    print(f"{subject_colors[subj]}{subj}{Colors.RESET}: {score_color}{self.to_full_width(score)}{Colors.RESET} [{rating_color}{rating}{Colors.RESET}] (权重: {weight}, 加权分: {score_color}{self.to_full_width(weighted_score):.1f}{Colors.RESET})")
            
            # 更新总分
            self.game_state['monthly_total_score'] = total_score
            
            if exam_type == 'monthly_day1':
                print(f"{Colors.CYAN}月考第一天结束，请在明天继续完成第二天的考试。{Colors.RESET}")
            else:  # monthly_day2
                # 考试完成，计算总排名
                max_total = min(750, total_score + 100)
                other_totals = [random.randint(300, int(max_total)) for _ in range(499)]
                all_totals = other_totals + [total_score]
                all_totals.sort(reverse=True)
                rank = all_totals.index(total_score) + 1
                
                self.game_state['exam_rank']['monthly'] = rank
                self.game_state['monthly_exam_complete'] = True
                
                # 总分和排名颜色
                total_color = Colors.GREEN if total_score >= 600 else Colors.BLUE if total_score >= 450 else Colors.RED
                rank_color = Colors.GREEN if rank <= 50 else Colors.BLUE if rank <= 200 else Colors.RED
                
                print(f"总分: {total_color}{self.to_full_width(total_score):.1f}{Colors.RESET}")
                print(f"年级排名: {rank_color}{self.to_full_width(rank)}{Colors.RESET}/{self.to_full_width(500)}")
                
                # 成绩影响
                if rank <= 50:
                    print(f"{Colors.GREEN}恭喜！你获得了'特级教师答疑'权限，可选择一门科目熟练度 +10。{Colors.RESET}")
                    # 让玩家选择科目
                    valid_choices = [subj for subj in self.subjects if self.subjects[subj] != -1]
                    if valid_choices:
                        print("请选择要增加熟练度的科目:")
                        for i, subj in enumerate(valid_choices):
                            print(f"{i+1}. {subj}")
                        try:
                            choice = int(input()) - 1
                            if 0 <= choice < len(valid_choices):
                                selected_subj = valid_choices[choice]
                                self.subjects[selected_subj] += 10
                                print(f"{selected_subj} 熟练度 +{self.to_full_width(10)}")
                            else:
                                print("输入无效，随机选择一门科目。")
                                selected_subj = random.choice(valid_choices)
                                self.subjects[selected_subj] += 10
                                print(f"{selected_subj} 熟练度 +{self.to_full_width(10)}")
                        except ValueError:
                            print("输入无效，随机选择一门科目。")
                            selected_subj = random.choice(valid_choices)
                            self.subjects[selected_subj] += 10
                            print(f"{selected_subj} 熟练度 +{self.to_full_width(10)}")
                elif rank >= 450:
                    print(f"{Colors.RED}成绩不理想，所有科目熟练度 -2。{Colors.RESET}")
                    for subj in self.subjects:
                        if self.subjects[subj] != -1:
                            self.subjects[subj] = max(0, self.subjects[subj] - 2)
            print(f"年级排名: {rank_color}{self.to_full_width(rank)}{Colors.RESET}/{self.to_full_width(500)}")
            
            # 成绩影响
            if rank <= 50:
                print("恭喜！你解锁了'特级教师答疑'权限，指定科目熟练度 ＋１０/次。")
                # 选择科目
                if self.game_state['science_arts'] == 'science':
                    subjects = ['语文', '数学', '英语', '物理', '化学', '生物']
                elif self.game_state['science_arts'] == 'arts':
                    subjects = ['语文', '数学', '英语', '政治', '历史', '地理']
                else:
                    subjects = list(self.subjects.keys())
                
                print("可选择的科目:")
                for i, subj in enumerate(subjects):
                    if self.subjects[subj] != -1:
                        print(f"{i+1}. {subj}")
                
                choice = int(input("请选择要答疑的科目: ")) - 1
                while choice < 0 or choice >= len(subjects) or self.subjects[subjects[choice]] == -1:
                    choice = int(input("输入无效，请重新选择: ")) - 1
                
                subj = subjects[choice]
                self.subjects[subj] += 10
                print(f"{subj} 熟练度 +{self.to_full_width(10)}")
        
        print("====================\n")
        input(f"{Colors.CYAN}按Enter键继续...{Colors.RESET}")

    def _take_final_exam(self, subjects):
        """进行期末考试"""
        total_score = 0
        valid_subjects = []
        
        if subjects:
            print(f"{Colors.LIGHT_YELLOW}各科成绩:{Colors.RESET}")
            for subj in subjects:
                if self.subjects[subj] != -1:
                    proficiency = self.subjects[subj]
                    status = (self.stats['自律性'] + self.stats['智力'] // 2) // 2
                    random_bonus = random.randint(1, 3)
                    # 语数英熟练度上限提高，调整计算系数以平衡分数
                    if subj in ['语文', '数学', '英语']:
                        score = int(proficiency * 0.7 + status * 0.25 + random_bonus)
                    else:
                        score = int(proficiency * 0.8 + status * 0.15 + random_bonus)
                    score = min(100, max(0, score))
                    
                    # 成绩颜色
                    score_color = Colors.GREEN if score >= 80 else Colors.BLUE if score >= 60 else Colors.RED
                    
                    # 获取评级
                    rating = self.get_rating(score)
                    rating_color = Colors.GREEN if rating in ['A', 'A+'] else Colors.BLUE if rating == 'B' else Colors.YELLOW if rating == 'C' else Colors.RED
                    
                    total_score += score
                    valid_subjects.append(subj)
                    
                    print(f"{subject_colors[subj]}{subj}{Colors.RESET}: {score_color}{self.to_full_width(score)}{Colors.RESET} [{rating_color}{rating}{Colors.RESET}]")
            
            # 计算平均分
            avg_score = total_score / len(valid_subjects) if valid_subjects else 0
            
            # 总分和平均分颜色
            total_color = Colors.GREEN if avg_score >= 80 else Colors.BLUE if avg_score >= 60 else Colors.RED
            
            print(f"今日考试总分: {total_color}{self.to_full_width(total_score)}{Colors.RESET}")
            print(f"今日考试平均分: {total_color}{self.to_full_width(avg_score):.1f}{Colors.RESET}")
            
            # 成绩影响
            if avg_score >= 80:
                print(f"{Colors.GREEN}恭喜！你获得了'优秀学生'称号，所有考试科目熟练度 +3。{Colors.RESET}")
                for subj in valid_subjects:
                    self.subjects[subj] += 3
            elif avg_score < 60:
                print(f"{Colors.RED}成绩不理想，需要寒假补课，压力值 +5。{Colors.RESET}")
                self.stats['压力值'] += 5
        else:
            print("当前没有需要考试的科目。")
        
        print("====================\n")
        input("按Enter键继续...")

    def holiday_effect(self):
        """假期效果"""
        print(f"{Colors.LIGHT_YELLOW}===== 假期效果 ====={Colors.RESET}")
        print("假期期间，你需要完成每日3小时自习。")
        
        # 假期属性变化
        self.stats['压力值'] = max(0, self.stats['压力值'] - 20)
        print(f"{Colors.GREEN}压力值 -{self.to_full_width(20)}，当前压力值: {self.to_full_width(self.stats['压力值'])}{Colors.RESET}")
        
        # 随机提升一门科目熟练度
        if self.game_state['science_arts'] == 'science':
            subjects = ['语文', '数学', '英语', '物理', '化学', '生物']
        elif self.game_state['science_arts'] == 'arts':
            subjects = ['语文', '数学', '英语', '政治', '历史', '地理']
        else:
            subjects = list(self.subjects.keys())
        
        subj = random.choice(subjects)
        while self.subjects[subj] == -1:
            subj = random.choice(subjects)
        
        self.subjects[subj] += 10
        print(f"{subject_colors[subj]}{subj}{Colors.RESET} 熟练度 +{Colors.GREEN}{self.to_full_width(10)}{Colors.RESET}")
        
        print(f"{Colors.LIGHT_YELLOW}===================={Colors.RESET}\n")
        input("按Enter键继续...")

    def check_attr_decay(self):
        """检查属性衰减"""
        # 社交属性衰减：连续7天未执行社交类行动，每日自动-1（最低降至30）
        self.game_state['last_social'] += 1
        if self.game_state['last_social'] >= 7:
            if self.stats['社交'] > 30:
                self.stats['社交'] -= 1
                print(f"{Colors.RED}社交属性衰减：连续{self.to_full_width(7)}天未社交，社交 -{self.to_full_width(1)}{Colors.RESET}")
        
        # 体能属性衰减：连续5天未执行运动类行动，每日自动-1（最低降至20）
        self.game_state['last_exercise'] += 1
        if self.game_state['last_exercise'] >= 5:
            if self.stats['体能'] > 20:
                self.stats['体能'] -= 1
                print(f"{Colors.RED}体能属性衰减：连续{self.to_full_width(5)}天未运动，体能 -{self.to_full_width(1)}{Colors.RESET}")
        
        # 学科熟练度衰减：连续14天未学习某科目，熟练度每日-2（最低降至10）
        for subj in self.subjects:
            if self.subjects[subj] != -1:
                self.game_state['last_study'][subj] += 1
                if self.game_state['last_study'][subj] >= 14:
                    if self.subjects[subj] > 10:
                        self.subjects[subj] = max(10, self.subjects[subj] - 2)
                        print(f"{subject_colors[subj]}{subj}{Colors.RESET} 熟练度衰减：连续{self.to_full_width(14)}天未学习，熟练度 -{Colors.RED}{self.to_full_width(2)}{Colors.RESET}")

    def check_game_over(self):
        """检查游戏是否结束"""
        # 检查是否到结束日期
        if self.game_state['current_date'] > datetime(2025, 6, 7):
            self.game_state['game_over'] = True
            self.calculate_ending()
            return True
        
        return False

    def calculate_ending(self):
        """计算结局"""
        print(f"\n{Colors.LIGHT_YELLOW}===== 高考结果 ====={Colors.RESET}")
        
        # 调用数值数据库中的结局计算函数
        ending = calculate_ending(self.subjects, self.stats)
        final_score = calculate_exam_score(self.subjects, self.stats, 'final')
        
        # 总分颜色
        score_color = Colors.GREEN if final_score >= 600 else Colors.BLUE if final_score >= 450 else Colors.RED
        
        print(f"高考总分: {score_color}{self.to_full_width(final_score)}{Colors.RESET}/{self.to_full_width(750)}")
        
        # 结局描述颜色
        if ending['type'] == 'excellent':
            desc_color = Colors.GREEN
            self.game_state['ending'] = 'elite'
        elif ending['type'] == 'good':
            desc_color = Colors.BLUE
            self.game_state['ending'] = 'normal'
        elif ending['type'] == 'average':
            desc_color = Colors.YELLOW
            self.game_state['ending'] = 'college'
        else:
            desc_color = Colors.RED
            self.game_state['ending'] = 'fail'
            print(f"{Colors.RED}很遗憾，你落榜了。{Colors.RESET}")
        
        print(f"{desc_color}{ending['desc']}{Colors.RESET}")
        
        print(f"{Colors.LIGHT_YELLOW}===================={Colors.RESET}\n")

    def is_vacation(self):
        """检查当前日期是否为假期"""
        date = self.game_state['current_date']
        year = date.year
        month = date.month
        day = date.day
        
        # 国庆假期: 10月1-3日
        if month == 10 and 1 <= day <= 3:
            return True
        
        # 寒假: 1月15日到2月23日
        if (month == 1 and day >= 15) or (month == 2 and day <= 23):
            return True
        
        # 高考结束: 6月7日之后
        if month == 6 and day > 7:
            return True
        
        return False
    
    def is_rest_day(self):
        """检查当前日期是否为休息日（双周的周日）"""
        date = self.game_state['current_date']
        weekday = date.weekday()  # 0=周一, 6=周日
        
        # 检查是否为周日
        if weekday != 6:
            return False
        
        # 每两周休息一次（计算当年的周数，偶数周休息）
        week_num = date.isocalendar()[1]
        return week_num % 2 == 0
    
    def next_day(self):
        """进入下一天"""
        # 推进日期
        self.game_state['current_date'] += timedelta(days=1)
        # 更新星期几 (1-7, 周一=1, 周日=7)
        self.game_state['current_day'] = self.game_state['current_date'].weekday() + 1

        
        # 取消每日体力恢复
        # self.stats['体力值'] = min(self.stats['体力上限'], self.stats['体力值'] + 15)
        
        # 恢复体力上限（如果之前被降低）
        if self.stats['体力上限'] < 30:
            self.stats['体力上限'] = 30
            # 体力上限已恢复，但不显示提示
        
        # 自然恢复压力值
        stress_recovery = 1
        if self.stats['体能'] >= 50:
            stress_recovery += 2
        self.stats['压力值'] = max(0, self.stats['压力值'] - stress_recovery)

        # 每日检查属性衰减
        self.check_attr_decay()
        
        # 检查游戏是否结束（到2025年6月9日高考结束）
        if self.game_state['current_date'] > datetime(2025, 6, 9):
            self.game_state['game_over'] = True
            self.calculate_ending()
            return

        # 检查是否为百日誓师日（当年高考前100天）
        current_year = self.game_state['current_date'].year
        hundred_days_before = datetime(current_year, 6, 7) - timedelta(days=100)
        if self.game_state['current_date'] == hundred_days_before:
            self.clear_screen()
            print(f"\n{Colors.LIGHT_RED}===== 百日誓师大会 ====={Colors.RESET}")
            print(f"{Colors.WHITE}今天是距离高考还有100天的日子，学校举行了隆重的百日誓师大会。")
            print("校长激情澎湃的演讲让你热血沸腾，同学们的呐喊声此起彼伏。")
            print("你握紧拳头，暗下决心一定要在剩下的100天里拼尽全力，不留遗憾！")
            print(f"{Colors.GREEN}自律性 +5{Colors.RESET}")
            self.stats['自律性'] += 5
            print(f"{Colors.LIGHT_RED}======================={Colors.RESET}\n")
            input(f"{Colors.CYAN}按Enter键继续...{Colors.RESET}")

        
        # 每周检查事件（周一）
        if self.game_state['current_date'].weekday() == 0:
            self.check_events()
        
        # 显示日期变化
        date_str = self.game_state['current_date'].strftime('%Y年%m月%d日')
        weekday_str = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][self.game_state['current_date'].weekday()]

        
        # 检查是否为假期
        if self.is_vacation():
            print(f"{Colors.YELLOW}今天是假期，好好休息吧！{Colors.RESET}")
        # 检查是否为休息日
        elif self.is_rest_day():
            print(f"{Colors.GREEN}今天是休息日，放松一下吧！{Colors.RESET}")

    def title_screen(self):
        """显示游戏标题页面"""
        while True:
            self.clear_screen()
            print(f"{Colors.LIGHT_YELLOW}===================================={Colors.RESET}")
            print(f"{Colors.LIGHT_YELLOW}             高三的逆袭               {Colors.RESET}")
            print(f"{Colors.LIGHT_YELLOW}         ～ 一年高三，冲刺高考 ～     {Colors.RESET}")
            print(f"{Colors.LIGHT_YELLOW}           Ver private_test       {Colors.RESET}")
            print(f"{Colors.LIGHT_YELLOW}===================================={Colors.RESET}")
            print(f"{Colors.CYAN}1. {Colors.WHITE}开始新游戏{Colors.RESET}")
            print(f"{Colors.CYAN}2. {Colors.WHITE}读取存档{Colors.RESET}")
            print(f"{Colors.CYAN}3. {Colors.WHITE}退出游戏{Colors.RESET}")
            print(f"{Colors.LIGHT_YELLOW}===================================={Colors.RESET}")
            
            try:
                choice = input("请选择操作 (输入1-3): ")
            except EOFError:
                # 处理无法获取标准输入的情况
                print(f"{Colors.RED}无法获取输入，程序将退出。{Colors.RESET}")
                time.sleep(2)
                exit()
            
            if choice == '1':
                self.start_new_game()
                break
            elif choice == '2':
                self.load_save()
                break
            elif choice == '3':
                print(f"{Colors.GREEN}感谢游玩！再见～{Colors.RESET}")
                exit()
            else:
                print(f"{Colors.RED}输入无效，请重新选择。{Colors.RESET}")
                time.sleep(1)

    def start_new_game(self):
        """开始新游戏"""
        # 初始化游戏状态
        self.__init__()
        
        self.clear_screen()
        print(f"{Colors.LIGHT_YELLOW}===== 高三的逆袭 ====={Colors.RESET}")
        print(f"{Colors.WHITE}时光荏苒，转眼已经到了高三。经过两年的努力，你在一中的学习生活即将进入最后的冲刺阶段。{Colors.RESET}")
        print(f"{Colors.WHITE}距离高考仅剩不到一年时间，这将是决定命运的关键一年。你必须合理安排时间，平衡学习与生活，向着理想的大学努力拼搏。{Colors.RESET}")
        print(f"{Colors.WHITE}通过选择不同的行动，提升自己的属性和学科熟练度，最终考上理想的大学。{Colors.RESET}")
        print(f"{Colors.LIGHT_YELLOW}============================={Colors.RESET}")
        
        # 加载DLC (隐藏显示)
        self.dlc_manager.load_dlcs(silent=True)
        
        # 选择文理科
        print(f"\n{Colors.LIGHT_YELLOW}===== 选择文理科 ====={Colors.RESET}")
        print(f"{Colors.CYAN}1. {Colors.WHITE}理科 (物理、化学、生物){Colors.RESET}")
        print(f"{Colors.CYAN}2. {Colors.WHITE}文科 (政治、历史、地理){Colors.RESET}")
        
        while True:
            choice = input(f"{Colors.CYAN}请选择文理科 (输入1-2): {Colors.RESET}")
            if choice == '1':
                self.game_state['science_arts'] = 'science'
                print(f"{Colors.GREEN}你选择了理科。高考将考察语文、数学、英语和物理、化学、生物。{Colors.RESET}")
                break
            elif choice == '2':
                self.game_state['science_arts'] = 'arts'
                print(f"{Colors.GREEN}你选择了文科。高考将考察语文、数学、英语和政治、历史、地理。{Colors.RESET}")
                break
            else:
                print(f"{Colors.RED}输入无效，请重新选择。{Colors.RESET}")
                time.sleep(1)
        
        # 根据选择设置科目
        if self.game_state['science_arts'] == 'science':
            # 理科：隐藏政治、历史、地理
            for subj in ['政治', '历史', '地理']:
                self.subjects[subj] = -1
        else:
            # 文科：隐藏物理、化学、生物
            for subj in ['物理', '化学', '生物']:
                self.subjects[subj] = -1
        
        # 初始事件
        print(f"\n{Colors.YELLOW}2024年9月2日，高三开学第一天：你怀着紧张而期待的心情踏入校园，开始了高考冲刺之旅。{Colors.RESET}")
        input(f"{Colors.CYAN}按Enter键开始游戏...{Colors.RESET}")
        
        # 进入主循环
        self.main_loop()

    def game_menu(self):
        """游戏菜单"""
        while True:
            self.clear_screen()
            print(f"{Colors.LIGHT_YELLOW}===================================={Colors.RESET}")
            print(f"{Colors.LIGHT_YELLOW}              游戏菜单                {Colors.RESET}")
            print(f"{Colors.LIGHT_YELLOW}===================================={Colors.RESET}")
            print(f"{Colors.CYAN}sv{Colors.RESET}. {Colors.WHITE}保存游戏进度{Colors.RESET}")
            print(f"{Colors.CYAN}ld{Colors.RESET}. {Colors.WHITE}加载游戏进度{Colors.RESET}")
            print(f"{Colors.CYAN}st{Colors.RESET}. {Colors.WHITE}游戏设置{Colors.RESET}")
            print(f"{Colors.CYAN}qt{Colors.RESET}. {Colors.WHITE}退出游戏{Colors.RESET}")
            print(f"{Colors.CYAN}bk{Colors.RESET}. {Colors.WHITE}返回游戏{Colors.RESET}")
            print(f"{Colors.CYAN}tt{Colors.RESET}. {Colors.WHITE}回到标题页面{Colors.RESET}")
            print(f"{Colors.LIGHT_YELLOW}===================================={Colors.RESET}")
            
            choice = input("请选择操作 (输入指令): ").lower()
            
            if choice == 'sv':
                self.save_game()
            elif choice == 'ld':
                self.load_save()
                break
            elif choice == 'st':
                self.game_settings()
            elif choice == 'qt':
                print("感谢游玩！再见～")
                exit()
            elif choice == 'bk':
                break
            elif choice == 'tt':
                self.title_screen()
                break
            else:
                print("输入无效，请重新选择。")
                time.sleep(1)

    def save_game(self):
        """保存游戏进度"""
        import os
        import json
        
        # 创建save文件夹（如果不存在）
        save_dir = os.path.join(os.path.dirname(__file__), 'save')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            print(f"{Colors.GREEN}已创建存档文件夹: {save_dir}{Colors.RESET}")
        
        # 准备存档数据 - 将datetime转换为字符串
        game_state_copy = self.game_state.copy()
        game_state_copy['current_date'] = game_state_copy['current_date'].isoformat()
        
        save_data = {
            'stats': self.stats,
            'subjects': self.subjects,
            'game_state': game_state_copy
        }
        
        # 保存到文件
        save_file = os.path.join(save_dir, 'save1.json')
        try:
            with open(save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=4)
            print(f"{Colors.GREEN}游戏进度已保存到: {save_file}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}保存失败: {str(e)}{Colors.RESET}")
        
        input("按Enter键继续...")

    def load_save(self):
        """读取存档 - 显示存档列表供用户选择"""
        import os
        import json
        from datetime import datetime
        
        self.clear_screen()
        print(f"{Colors.LIGHT_YELLOW}===== 读取存档 ====={Colors.RESET}")
        
        # 检查save文件夹是否存在
        save_dir = os.path.join(os.path.dirname(__file__), 'save')
        if not os.path.exists(save_dir):
            print(f"{Colors.RED}存档文件夹不存在，无法读取存档。{Colors.RESET}")
            input(f"{Colors.CYAN}按Enter键返回菜单...{Colors.RESET}")
            return
        
        # 获取所有存档文件
        save_files = [f for f in os.listdir(save_dir) if f.endswith('.json')]
        
        if not save_files:
            print(f"{Colors.RED}当前暂无可用存档。{Colors.RESET}")
            input(f"{Colors.CYAN}按Enter键返回菜单...{Colors.RESET}")
            return
        
        # 显示存档列表
        print(f"{Colors.LIGHT_YELLOW}可用存档:{Colors.RESET}")
        for i, file in enumerate(save_files, 1):
            print(f"{i}. {file}")
        
        # 让用户选择存档
        while True:
            choice = input(f"{Colors.CYAN}请选择要加载的存档 (输入序号或'tt'返回): {Colors.RESET}")
            if choice.lower() == 'tt':
                return
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(save_files):
                    save_file = os.path.join(save_dir, save_files[choice_num-1])
                    break
                else:
                    print(f"{Colors.RED}输入无效，请重新选择。{Colors.RESET}")
            except ValueError:
                print(f"{Colors.RED}请输入有效的数字或'tt'返回。{Colors.RESET}")
        
        # 读取选中的存档
        try:
            with open(save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # 恢复游戏状态
            self.stats = save_data['stats']
            self.subjects = save_data['subjects']
            self.game_state = save_data['game_state']
            
            # 将字符串转换为datetime对象
            self.game_state['current_date'] = datetime.fromisoformat(self.game_state['current_date'])
            
            # 确保current_day存在
            if 'current_day' not in self.game_state:
                self.game_state['current_day'] = self.game_state['current_date'].weekday() + 1  # 1-7, 周一=1, 周日=7

            # 确保disable_screen_clear存在
            if 'disable_screen_clear' not in self.game_state:
                self.game_state['disable_screen_clear'] = False
            
            print(f"{Colors.GREEN}存档 {save_files[choice-1]} 读取成功！{Colors.RESET}")
            
            # 初始化DLC管理器并加载DLC
            self.dlc_manager = DLCManager(self)
            self.dlc_manager.load_dlcs()
            
            input(f"{Colors.CYAN}按Enter键开始游戏...{Colors.RESET}")
            
            # 进入游戏主循环
            self.main_loop()
        except Exception as e:
            print(f"{Colors.RED}读取失败: {str(e)}{Colors.RESET}")
            input(f"{Colors.CYAN}按Enter键返回菜单...{Colors.RESET}")

    def game_settings(self):
        """游戏设置"""
        self.clear_screen()
        print(f"{Colors.LIGHT_YELLOW}===== 游戏设置 ====={Colors.RESET}")
        # 根据设置显示不同颜色
        if self.game_state.get('disable_screen_clear', False):
            print(f"{Colors.RED}1. 不启用刷新屏幕: 开启{Colors.RESET}")
        else:
            print(f"{Colors.GREEN}1. 不启用刷新屏幕: 关闭{Colors.RESET}")
        print(f"{Colors.WHITE}2. 回到主菜单{Colors.RESET}")
        
        choice = input(f"{Colors.CYAN}请选择设置项 (输入1-2): {Colors.RESET}")
        
        if choice == '2':
            return
        elif choice == '1':
            # 切换不启用刷新屏幕的状态
            self.game_state['disable_screen_clear'] = not self.game_state['disable_screen_clear']
            status = '开启' if self.game_state['disable_screen_clear'] else '关闭'
            color = Colors.RED if self.game_state['disable_screen_clear'] else Colors.GREEN
            print(f"{color}不启用刷新屏幕已{status}{Colors.RESET}")
            # 保存设置
            self.save_game()
            input(f"{Colors.CYAN}按Enter键返回...{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}无效的选择，请重新输入。{Colors.RESET}")
            input(f"{Colors.CYAN}按Enter键返回...{Colors.RESET}")

    def main_loop(self):
        """游戏主循环"""
        while not self.game_state['game_over']:
            # 打印状态
            self.print_status()
            

            
            # 根据当前状态选择行动列表
            is_vacation = self.is_vacation()
            is_rest_day = self.is_rest_day()
            
            if is_vacation:
                self.actions = self.vacation_actions.copy()
                print(f"{Colors.YELLOW}===== 假期行动 ====={Colors.RESET}")
            elif is_rest_day:
                # 休息日减少学习行动，增加休闲行动
                self.actions = [action for action in self.normal_actions if action['type'] != 'study']
                # 在休息日添加周末补课行动
                weekend_study_action = {'name': '周末补课', 'cost': 12, 'desc': '薄弱科目熟练度 ＋８，体力值上限 －２（次日恢复）', 'type': 'study'}
                self.actions.append(weekend_study_action)
                self.actions.append({'name': '户外游玩', 'cost': 5, 'desc': '体能 ＋２，社交 ＋３，压力值 －７', 'type': 'social'})
                self.actions.append({'name': '在家追剧', 'cost': 0, 'desc': '压力值 －６，自律性 －１', 'type': 'rest'})
                print(f"{Colors.GREEN}===== 休息日行动 ====={Colors.RESET}")
            else:
                self.actions = self.normal_actions.copy()
                print(f"{Colors.LIGHT_YELLOW}可用行动:{Colors.RESET}")
            
            # 显示可用行动
            for i, action in enumerate(self.actions):
                print(f"{Colors.CYAN}{self.to_full_width(i+1)}{Colors.RESET}. {Colors.WHITE}{action['name']}{Colors.RESET} (体力消耗: {Colors.GREEN}{self.to_full_width(action['cost'])}{Colors.RESET}) - {action['desc']}")
            
            # 检查是否为周测时间（周一）
            is_exam_day = self.game_state['current_date'].weekday() == 0
            # 排除特殊日期的周测
            is_first_week = self.game_state['current_date'].month == 9 and self.game_state['current_date'].day == 2
            is_first_day_after_vacation = self.game_state['current_date'].month == 2 and self.game_state['current_date'].day == 24
            if is_exam_day and not self.is_vacation() and not self.is_rest_day() and not is_first_week and not is_first_day_after_vacation and not is_monthly_exam:
                print(f"{Colors.RED}今天是周测日，必须参加周测！{Colors.RESET}")
                self.take_exam('weekly')
                self.game_state['actions_today'] = 1  # 周测消耗所有行动次数
                self.next_day()  # 推进到下一天
                continue

            # 检查是否为期末考试时间（1月13~14日）
            is_final_exam_day = self.game_state['current_date'].month == 1 and 13 <= self.game_state['current_date'].day <= 14
            if is_final_exam_day and not self.is_vacation() and not self.is_rest_day():
                exam_day = self.game_state['current_date'].day
                subjects_text = "语数英" if exam_day == 13 else "物化生/政史地"
                print(f"{Colors.CYAN}{self.to_full_width(len(self.actions)+2)}{Colors.RESET}. {Colors.WHITE}参加期末考试（{subjects_text}）{Colors.RESET}")

            # 检查是否为月考时间（每月最后一周的周四和周五）
            is_monthly_exam = False
            monthly_exam_day = 0
            # 获取当月最后一天
            last_day = calendar.monthrange(self.game_state['current_date'].year, self.game_state['current_date'].month)[1]
            last_date = date(self.game_state['current_date'].year, self.game_state['current_date'].month, last_day)
            # 计算最后一个周五
            days_to_friday = (4 - last_date.weekday() + 7) % 7
            last_friday = last_date - timedelta(days=days_to_friday)
            # 最后一个周四
            last_thursday = last_friday - timedelta(days=1)
            # 检查是否是月考日
            if self.game_state['current_date'] == last_thursday and not self.is_vacation() and not self.is_rest_day():
                is_monthly_exam = True
                monthly_exam_day = 1
            elif self.game_state['current_date'] == last_friday and not self.is_vacation() and not self.is_rest_day():
                is_monthly_exam = True
                monthly_exam_day = 2
            # 显示月考选项
            if is_monthly_exam:
                subjects_text = "语数英" if monthly_exam_day == 1 else "物化生/政史地"
                print(f"{Colors.CYAN}{self.to_full_width(len(self.actions)+3)}{Colors.RESET}. {Colors.WHITE}参加月考（{subjects_text}）{Colors.RESET}")
            
            # 让玩家选择行动
            choice = input(f"{Colors.CYAN}请选择行动 (输入编号，或输入'opt'打开菜单): {Colors.RESET}")
            
            # 检查是否打开菜单
            if choice.lower() == 'opt':
                self.game_menu()
                continue
            
            # 处理月考
            if is_monthly_exam and choice == str(len(self.actions)+3):
                exam_type = 'monthly_day1' if monthly_exam_day == 1 else 'monthly_day2'
                self.take_exam(exam_type)
                self.game_state['actions_today'] = 1  # 考试消耗所有行动次数


                self.game_state['actions_today'] = 1  # 周测消耗所有行动次数

            # 处理期末考试
            is_final_exam_day = self.game_state['current_date'].month == 1 and 13 <= self.game_state['current_date'].day <= 14
            if is_final_exam_day and choice == str(len(self.actions)+2):
                exam_type = 'final_day1' if self.game_state['current_date'].day == 13 else 'final_day2'
                self.take_exam(exam_type)
                self.game_state['actions_today'] = 1  # 考试消耗所有行动次数
            else:
                try:
                    action_idx = int(choice) - 1
                    # 检查选择是否有效
                    valid = False
                    if 0 <= action_idx < len(self.actions):
                        action = self.actions[action_idx]
                        # 检查行动是否受时间限制
                        # 由于只有在休息日才会显示周末补课选项，这里可以省略条件检查
                        # if action['name'] == '周末补课' and self.game_state['current_day'] != 7:
                        #     print("周末补课只能在周日执行。")
                        if action['name'] == '晚自习复盘' and self.game_state['current_day'] > 4:
                            print("晚自习复盘只能在周一至周四执行。")
                        else:
                            valid = True
                    
                    if valid:
                        success = self.take_action(action_idx)
                        if success:
                            # 重置对应计数器
                            if self.actions[action_idx]['type'] == 'social':
                                self.game_state['last_social'] = 0
                            elif self.actions[action_idx]['type'] == 'exercise':
                                self.game_state['last_exercise'] = 0
                            elif self.actions[action_idx]['type'] == 'study':
                                # 如果是学习行动，重置对应科目的学习计数器
                                # (这里简化处理，实际应该根据选择的科目来重置)
                                for subj in self.subjects:
                                    if self.subjects[subj] != -1:
                                        self.game_state['last_study'][subj] = 0
                    else:
                        print("输入无效，请重新选择。")
                except ValueError:
                    print("输入无效，请输入数字。")
            
            # 已在next_day方法中检查属性衰减，此处不再检查
            # self.check_attr_decay()
            
            # 检查游戏是否结束
            if self.check_game_over():
                break
            
            # 先显示按Enter提示，再清屏
            input("按Enter键继续...")
            self.clear_screen()
        
        # 游戏结束，显示结局
        self.clear_screen()
        print(f"\n{Colors.LIGHT_YELLOW}===== 游戏结束 ====={Colors.RESET}")
        if self.game_state['ending'] == 'elite':
            print(f"{Colors.GREEN}结局：名校录取 | 你凭借优异的成绩和全面的素质，被顶尖名校录取。未来的人生一片光明！{Colors.RESET}")
        elif self.game_state['ending'] == 'normal':
            print(f"{Colors.BLUE}结局：普通本科录取 | 你通过自己的努力，考上了一所不错的本科院校。继续加油！{Colors.RESET}")
        elif self.game_state['ending'] == 'college':
            print(f"{Colors.YELLOW}结局：专科录取 | 你被专科院校录取了。这只是人生的一个阶段，未来仍有无限可能。{Colors.RESET}")
        elif self.game_state['ending'] == 'dropout':
            print(f"{Colors.RED}结局：辍学 | 由于长期压力过大且未能调整，你选择了辍学。人生道路千万条，重新出发依然有希望。{Colors.RESET}")
        else:
            print(f"{Colors.RED}结局：落榜 | 很遗憾，你未能考上理想的大学。不要灰心，人生还有很多其他的选择和机会。{Colors.RESET}")
        print(f"{Colors.LIGHT_YELLOW}===================={Colors.RESET}")

    def run(self):
        """运行游戏"""
        # 调试：显示DLC加载状态
        print("\n[调试信息] 游戏启动中...")
        if hasattr(self, 'dlc_manager'):
            print(f"[调试信息] DLC管理器已初始化")
            # 显示已加载的DLC数量
            dlc_count = len(self.dlc_manager.get_installed_dlcs())
            print(f"[调试信息] 已加载 {dlc_count} 个DLC")
            # 显示常规行动列表
            normal_actions = [action['name'] for action in self.normal_actions]
            print(f"[调试信息] 常规行动列表 ({len(normal_actions)}): {normal_actions}")
            # 显示假期行动列表
            vacation_actions = [action['name'] for action in self.vacation_actions]
            print(f"[调试信息] 假期行动列表 ({len(vacation_actions)}): {vacation_actions}")
        else:
            print("[调试信息] DLC管理器未初始化")
        
        self.title_screen()

if __name__ == '__main__':
    game = HighSchoolSimulator()
    game.run()