#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DLC扩展管理器 - 用于加载和管理游戏的DLC内容
"""
import os
import json
from datetime import datetime, timedelta

class DLCManager:
    def __init__(self, game_instance):
        """初始化DLC管理器
        
        Args:
            game_instance: HighSchoolSimulator游戏实例
        """
        self.game = game_instance
        self.dlcs = {}
        self.dlc_dir = os.path.join(os.path.dirname(__file__), 'dlc')
        
        # 创建DLC目录（如果不存在）
        if not os.path.exists(self.dlc_dir):
            os.makedirs(self.dlc_dir)
            print(f"已创建DLC目录: {self.dlc_dir}")

    def load_dlcs(self, silent=False):
        """加载所有已安装的DLC

        Args:
            silent: 是否静默加载，不输出信息
        """
        if not os.path.exists(self.dlc_dir):
            if not silent:
                print("DLC目录不存在，无法加载DLC。")
            return

        # 获取所有DLC文件夹
        dlc_folders = [f for f in os.listdir(self.dlc_dir) if os.path.isdir(os.path.join(self.dlc_dir, f))]

        if not dlc_folders:
            if not silent:
                print("当前暂无安装的DLC。")
            return

        for dlc_name in dlc_folders:
            dlc_path = os.path.join(self.dlc_dir, dlc_name)
            manifest_file = os.path.join(dlc_path, 'manifest.json')
            
            if not os.path.exists(manifest_file):
                if not silent:
                    print(f"DLC {dlc_name} 缺少manifest.json文件，跳过加载。")
                continue

            try:
                with open(manifest_file, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)

                # 验证manifest格式
                if 'name' not in manifest or 'version' not in manifest:
                    if not silent:
                        print(f"DLC {dlc_name} 的manifest.json格式不正确，跳过加载。")
                    continue

                # 存储DLC信息
                self.dlcs[dlc_name] = {
                    'manifest': manifest,
                    'path': dlc_path
                }

                # 调用DLC的初始化函数（如果有）
                if 'init_script' in manifest:
                    init_script = os.path.join(dlc_path, manifest['init_script'])
                    if os.path.exists(init_script):
                        self._load_script(init_script, dlc_name)

                if not silent:
                    print(f"成功加载DLC: {manifest['name']} (v{manifest['version']})")
            except Exception as e:
                print(f"加载DLC {dlc_name} 时出错: {str(e)}")

    def _load_script(self, script_path, dlc_name):
        """加载DLC脚本文件
        
        Args:
            script_path: 脚本文件路径
            dlc_name: DLC名称
        """
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                script_code = f.read()

            # 创建一个安全的执行环境
            local_vars = {
                'game': self.game,
                'dlc_manager': self,
                'datetime': datetime,
                'timedelta': timedelta
            }

            # 执行脚本
            exec(script_code, {}, local_vars)
        except Exception as e:
            print(f"执行DLC {dlc_name} 的脚本时出错: {str(e)}")

    def register_action(self, action, action_type='normal'):
        """注册新行动
        
        Args:
            action: 行动字典, 包含'name', 'cost', 'desc', 'type'等键
            action_type: 行动类型, 'normal'或'vacation'
        """
        if action_type == 'normal':
            # 检查行动是否已存在
            for existing_action in self.game.normal_actions:
                if existing_action['name'] == action['name']:
                    print(f"行动 '{action['name']}' 已存在于常规行动列表中，跳过注册。")
                    return
            self.game.normal_actions.append(action)
            print(f"成功注册常规行动: {action['name']}")
        elif action_type == 'vacation':
            # 检查行动是否已存在
            for existing_action in self.game.vacation_actions:
                if existing_action['name'] == action['name']:
                    print(f"行动 '{action['name']}' 已存在于假期行动列表中，跳过注册。")
                    return
            self.game.vacation_actions.append(action)
            print(f"成功注册假期行动: {action['name']}")
        else:
            print(f"无效的行动类型: {action_type}，请使用'normal'或'vacation'。")

    def register_event(self, event, event_type='random'):
        """注册新事件
        
        Args:
            event: 事件字典, 包含'condition', 'prob', 'desc', 'effect'等键
            event_type: 事件类型, 'fixed'或'random'
        """
        if event_type == 'fixed':
            # 固定事件需要额外的'month'和'week'字段
            if 'month' not in event or 'week' not in event:
                print("固定事件必须包含'month'和'week'字段。")
                return
            self.game.events['fixed'].append(event)
            print(f"成功注册固定事件: {event['desc'][:20]}...")
        elif event_type == 'random':
            # 随机事件需要'condition', 'prob', 'desc', 'effect'字段
            required_fields = ['condition', 'prob', 'desc', 'effect']
            for field in required_fields:
                if field not in event:
                    print(f"随机事件必须包含'{field}'字段。")
                    return
            self.game.events['random'].append(event)
            print(f"成功注册随机事件: {event['desc'][:20]}...")
        else:
            print(f"无效的事件类型: {event_type}，请使用'fixed'或'random'")

    def register_ending(self, ending_id, ending_desc, condition_func):
        """注册新结局
        
        Args:
            ending_id: 结局ID
            ending_desc: 结局描述
            condition_func: 判断结局的条件函数, 接受stats和subjects参数
        """
        # 存储结局信息（在实际游戏中可能需要扩展calculate_ending函数来使用这些结局）
        if not hasattr(self.game, 'dlc_endings'):
            self.game.dlc_endings = {}
        self.game.dlc_endings[ending_id] = {
            'desc': ending_desc,
            'condition': condition_func
        }
        print(f"成功注册结局: {ending_id}")

    def get_installed_dlcs(self):
        """获取所有已安装的DLC列表
        
        Returns:
            list: 包含所有DLC名称的列表
        """
        return list(self.dlcs.keys())

    def get_dlc_info(self, dlc_name):
        """获取特定DLC的信息
        
        Args:
            dlc_name: DLC名称
        
        Returns:
            dict: DLC信息字典, 如果DLC不存在则返回None
        """
        return self.dlcs.get(dlc_name)