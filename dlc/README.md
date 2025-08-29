# DLC开发指南

欢迎使用一中模拟器的DLC扩展系统！本指南将帮助你创建和使用自己的DLC。

## DLC目录结构

每个DLC需要放在`dlc`目录下，使用独立的文件夹。一个典型的DLC目录结构如下：

```
dlc/
└── your_dlc_name/
    ├── manifest.json    # DLC配置文件
    └── init_script.py   # DLC初始化脚本
```

## manifest.json格式

`manifest.json`是DLC的配置文件，包含以下字段：

```json
{
    "name": "DLC名称",
    "version": "版本号",
    "description": "DLC描述",
    "author": "作者名称",
    "init_script": "初始化脚本文件名"
}
```

## init_script.py格式

`init_script.py`是DLC的初始化脚本，用于注册新的行动、事件和结局。脚本需要包含一个`init_dlc`函数，该函数接收两个参数：`game`（游戏实例）和`dlc_manager`（DLC管理器实例）。

示例：

```python
def init_dlc(game, dlc_manager):
    # 添加新的常规行动
    new_action = {
        'name': '行动名称',
        'cost': 行动消耗,
        'desc': '行动描述',
        'type': '行动类型'  # study, social, exercise等
    }
    dlc_manager.register_action(new_action, 'normal')  # 注册到常规行动
    
    # 添加新的假期行动
    vacation_action = {
        'name': '假期行动名称',
        'cost': 行动消耗,
        'desc': '行动描述',
        'type': '行动类型'
    }
    dlc_manager.register_action(vacation_action, 'vacation')  # 注册到假期行动
    
    # 添加新的随机事件
    random_event = {
        'condition': lambda stats: 条件函数,
        'prob': 触发概率,
        'desc': '事件描述',
        'effect': lambda stats: 效果函数
    }
    dlc_manager.register_event(random_event, 'random')
    
    # 添加新的固定事件
    fixed_event = {
        'month': 月份,
        'week': 周数,
        'desc': '事件描述',
        'effect': '效果类型'  # 'none'或自定义效果
    }
    dlc_manager.register_event(fixed_event, 'fixed')
    
    # 添加新的结局
    new_ending = {
        'name': '结局名称',
        'condition': lambda stats, subjects: 条件函数,
        'desc': '结局描述'
    }
    dlc_manager.register_ending(new_ending)
```

## 测试DLC

1. 将你的DLC文件夹放在`dlc`目录下
2. 启动游戏，游戏会自动加载所有DLC
3. 在游戏中查看是否有新的行动、事件或结局

## 示例DLC

本项目提供了一个示例DLC`sports_club`（体育俱乐部），你可以参考它来创建自己的DLC。

## 注意事项

1. 确保你的DLC不会与游戏原有内容冲突
2. 不要修改游戏主文件，所有修改都应该通过DLC实现
3. 如果你的DLC需要添加新的属性或科目，请确保在游戏中有相应的处理逻辑

祝你开发愉快！
