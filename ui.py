import curses
import time


COLOR_PAIRS = {
    'RED': 1,           # 亮红
    'GREEN': 2,         # 亮绿
    'YELLOW': 3,        # 亮黄
    'BLUE': 4,          # 亮蓝
    'MAGENTA': 5,       # 亮品红
    'CYAN': 6,          # 亮青
    'WHITE': 7,         # 亮白
    'BROWN': 8,         # 亮棕
    'LIGHT_BLUE': 9,    # 更亮的蓝
    'DARK_BLUE': 10,    # 亮蓝
    'GRAY': 11,         # 亮灰
    'LIGHT_YELLOW': 12, # 更亮的黄
    'LIGHT_GREEN': 13,  # 更亮的绿
    'SKY_BLUE': 14      # 天蓝
}

# 窗口配置字典（纯净模板）
window_configs = {
    "main_menu": {
        "title": {
            "text": "",           # 窗口标题文本
            "position": "",       # 标题位置：center, left, right
            "attributes": [],     # 标题属性：bold, underline, reverse等
            "color": 0            # 标题颜色对编号
        },
        "size": {
            "height": 0,          # 窗口高度
            "width": 0,           # 窗口宽度
            "y": 0,               # 窗口起始行
            "x": 0                # 窗口起始列
        },
        "items": [                # 选项列表，每个选项是一个字典
            {
                "text": "",       # 选项显示的文本
                "action": None,   # 触发时调用的函数
                "help": "",       # 帮助提示文本
                "shortcut": "",   # 快捷键
                "color": 0,       # 颜色对编号
                "highlight_color": 0  # 高亮时的颜色对编号
            }
        ]
    }
}

window_configs_example = {
    "time": {
        "title": {
            "text": "状态   ",
            "position": "center",
            "attributes": ["bold"],
            "color": 3  # 标题颜色
        },
        "size": {
            "height": 7,
            "width": 30,
            "y": 3,
            "x": 3
        },
        "items": [
            {
                "text": "日期",
                "action": lambda: "游戏开始",
                "help": "开始新的游戏",
                "shortcut": "1",
                "color": 1,          # 普通状态颜色
                "highlight_color": 4 # 高亮状态颜色
            },
            {
                "text": "距离高考还剩",
                "action": lambda: "打开设置",
                "help": "调整游戏设置",
                "shortcut": "2",
                "color": 1,
                "highlight_color": 2
            },
            {
                "text": "今天是",
                "action": lambda: "打开设置",
                "help": "调整游戏设置",
                "shortcut": "2",
                "color": 1,
                "highlight_color": 2
            }
        ]
        },
    "attribute": {
        "title": {
            "text": "属性  ",           # 窗口标题文本
            "position": "",       # 标题位置：center, left, right
            "attributes": [],     # 标题属性：bold, underline, reverse等
            "color": 0            # 标题颜色对编号
        },
        "size": {
            "height": 11,          # 窗口高度
            "width": 30,           # 窗口宽度
            "y": 10,               # 窗口起始行
            "x": 3                # 窗口起始列
        },
        "items": [                # 选项列表，每个选项是一个字典
            {
                "text": "智力",
                "action": lambda: "退出游戏",
                "help": "退出游戏",
                "shortcut": "3",
                "color": 1,
                "highlight_color": 2
            },
            {
                "text": "记忆力",
                "action": lambda: "退出游戏",
                "help": "退出游戏",
                "shortcut": "3",
                "color": 1,
                "highlight_color": 2
            },
            {
                "text": "体能",
                "action": lambda: "退出游戏",
                "help": "退出游戏",
                "shortcut": "3",
                "color": 1,
                "highlight_color": 2
            },
            {
                "text": "社交",
                "action": lambda: "退出游戏",
                "help": "退出游戏",
                "shortcut": "3",
                "color": 1,
                "highlight_color": 2
            },
            {
                "text": "自律",
                "action": lambda: "退出游戏",
                "help": "退出游戏",
                "shortcut": "3",
                "color": 1,
                "highlight_color": 2
            },
            {
                "text": "压力",
                "action": lambda: "退出游戏",
                "help": "退出游戏",
                "shortcut": "3",
                "color": 1,
                "highlight_color": 2
            },
            {
                "text": "体力",
                "action": lambda: "退出游戏",
                "help": "退出游戏",
                "shortcut": "3",
                "color": 1,
                "highlight_color": 2
            }
        ]
        },
    "class": {
        "title": {
            "text": "课程熟练度  ",           # 窗口标题文本
            "position": "",       # 标题位置：center, left, right
            "attributes": [],     # 标题属性：bold, underline, reverse等
            "color": 0            # 标题颜色对编号
        },
        "size": {
            "height": 10,          # 窗口高度
            "width": 30,           # 窗口宽度
            "y": 21,               # 窗口起始行
            "x": 3                # 窗口起始列
        },
        "items": [                # 选项列表，每个选项是一个字典
            {
                "text": "语文",
                "action": lambda: "退出游戏",
                "help": "退出游戏",
                "shortcut": "3",
                "color": 1,
                "highlight_color": 2
            },
            {
                "text": "数学",
                "action": lambda: "退出游戏",
                "help": "退出游戏",
                "shortcut": "3",
                "color": 1,
                "highlight_color": 2
            },
            {
                "text": "英语",
                "action": lambda: "退出游戏",
                "help": "退出游戏",
                "shortcut": "3",
                "color": 1,
                "highlight_color": 2
            },
            {
                "text": "物理",
                "action": lambda: "退出游戏",
                "help": "退出游戏",
                "shortcut": "3",
                "color": 1,
                "highlight_color": 2
            },
            {
                "text": "化学",
                "action": lambda: "退出游戏",
                "help": "退出游戏",
                "shortcut": "3",
                "color": 1,
                "highlight_color": 2
            },
            {
                "text": "生物",
                "action": lambda: "退出游戏",
                "help": "退出游戏",
                "shortcut": "3",
                "color": 1,
                "highlight_color": 2
            },
        ]
        },


        "action": {
        "title": {
            "text": "可用行动      ",           # 窗口标题文本
            "position": "",       # 标题位置：center, left, right
            "attributes": [],     # 标题属性：bold, underline, reverse等
            "color": 0            # 标题颜色对编号
        },
        "size": {
            "height": 18,          # 窗口高度
            "width": 30,           # 窗口宽度
            "y": 3,               # 窗口起始行
            "x": 33                # 窗口起始列
        },
        "items": [                # 选项列表，每个选项是一个字典
            {
                "text": "早自习刷题",       # 选项显示的文本
                "action": None,   # 触发时调用的函数
                "help": "",       # 帮助提示文本
                "shortcut": "",   # 快捷键
                "color": 0,       # 颜色对编号
                "highlight_color": 0  # 高亮时的颜色对编号
            },
            {
                "text": "早自习刷题",       # 选项显示的文本
                "action": None,   # 触发时调用的函数
                "help": "",       # 帮助提示文本
                "shortcut": "",   # 快捷键
                "color": 0,       # 颜色对编号
                "highlight_color": 0  # 高亮时的颜色对编号
            }
        ]
    },
    "echo": {
        "title": {
            "text": "属性  ",           # 窗口标题文本
            "position": "",       # 标题位置：center, left, right
            "attributes": [],     # 标题属性：bold, underline, reverse等
            "color": 0            # 标题颜色对编号
        },
        "size": {
            "height": 10,          # 窗口高度
            "width": 30,           # 窗口宽度
            "y": 21,               # 窗口起始行
            "x": 33                # 窗口起始列
        },
        "items": [                # 选项列表，每个选项是一个字典
            {
                "text": "智力",
                "action": lambda: "退出游戏",
                "help": "退出游戏",
                "shortcut": "3",
                "color": 1,
                "highlight_color": 2
            },
        ]
        },
    "hint": {
        "title": {
            "text": "提示  ",           # 窗口标题文本
            "position": "",       # 标题位置：center, left, right
            "attributes": [],     # 标题属性：bold, underline, reverse等
            "color": 0            # 标题颜色对编号
        },
        "size": {
            "height": 5,          # 窗口高度
            "width": 60,           # 窗口宽度
            "y": 31,               # 窗口起始行
            "x": 3                # 窗口起始列
        },
        "items": [                # 选项列表，每个选项是一个字典
            {
                "text": "智力",
                "action": lambda: "退出游戏",
                "help": "退出游戏",
                "shortcut": "3",
                "color": 1,
                "highlight_color": 2
            },
        ]
        }
}

def init_colors():
    """初始化颜色对"""
    # 检查终端是否支持颜色
    if not curses.has_colors():
        return False
    
    # 启用颜色功能
    curses.start_color()
    
    # 使用默认颜色作为背景
    curses.use_default_colors()
    
    # 初始化颜色对
    # 基本颜色
    curses.init_pair(COLOR_PAIRS['RED'], curses.COLOR_RED, -1)        # 亮红
    curses.init_pair(COLOR_PAIRS['GREEN'], curses.COLOR_GREEN, -1)    # 亮绿
    curses.init_pair(COLOR_PAIRS['YELLOW'], curses.COLOR_YELLOW, -1)  # 亮黄
    curses.init_pair(COLOR_PAIRS['BLUE'], curses.COLOR_BLUE, -1)      # 亮蓝
    curses.init_pair(COLOR_PAIRS['MAGENTA'], curses.COLOR_MAGENTA, -1) # 亮品红
    curses.init_pair(COLOR_PAIRS['CYAN'], curses.COLOR_CYAN, -1)      # 亮青
    curses.init_pair(COLOR_PAIRS['WHITE'], curses.COLOR_WHITE, -1)    # 亮白
    
    # 如果支持256色，定义更多颜色
    if curses.COLORS >= 256:
        # 棕色 (ANSI 173)
        curses.init_color(100, 1000, 750, 500)  # 自定义颜色索引100为棕色
        curses.init_pair(COLOR_PAIRS['BROWN'], 100, -1)  # 亮棕
        
        # 更亮的蓝 (ANSI 159)
        curses.init_color(101, 750, 1000, 1000) # 自定义颜色索引101为更亮的蓝
        curses.init_pair(COLOR_PAIRS['LIGHT_BLUE'], 101, -1)  # 更亮的蓝
        
        # 亮蓝 (ANSI 75) - 替换暗蓝
        curses.init_color(102, 250, 750, 1000)  # 自定义颜色索引102为亮蓝
        curses.init_pair(COLOR_PAIRS['DARK_BLUE'], 102, -1)  # 亮蓝
        
        # 亮灰 (ANSI 245)
        curses.init_color(103, 750, 750, 750)   # 自定义颜色索引103为亮灰
        curses.init_pair(COLOR_PAIRS['GRAY'], 103, -1)  # 亮灰
        
        # 更亮的黄 (ANSI 228)
        curses.init_color(104, 1000, 1000, 750) # 自定义颜色索引104为更亮的黄
        curses.init_pair(COLOR_PAIRS['LIGHT_YELLOW'], 104, -1)  # 更亮的黄
        
        # 更亮的绿 (ANSI 120)
        curses.init_color(105, 750, 1000, 750)  # 自定义颜色索引105为更亮的绿
        curses.init_pair(COLOR_PAIRS['LIGHT_GREEN'], 105, -1)  # 更亮的绿
        
        # 更亮的天蓝 (ANSI 153)
        curses.init_color(106, 750, 850, 1000)  # 自定义颜色索引106为天蓝
        curses.init_pair(COLOR_PAIRS['SKY_BLUE'], 106, -1)  # 天蓝
    else:
        # 如果不支持256色，使用近似的基本颜色
        curses.init_pair(COLOR_PAIRS['BROWN'], curses.COLOR_YELLOW, -1)     # 棕色 -> 黄色
        curses.init_pair(COLOR_PAIRS['LIGHT_BLUE'], curses.COLOR_CYAN, -1)  # 更亮的蓝 -> 青色
        curses.init_pair(COLOR_PAIRS['DARK_BLUE'], curses.COLOR_BLUE, -1)   # 亮蓝 -> 蓝色
        curses.init_pair(COLOR_PAIRS['GRAY'], curses.COLOR_WHITE, -1)       # 亮灰 -> 白色
        curses.init_pair(COLOR_PAIRS['LIGHT_YELLOW'], curses.COLOR_YELLOW, -1)  # 更亮的黄 -> 黄色
        curses.init_pair(COLOR_PAIRS['LIGHT_GREEN'], curses.COLOR_GREEN, -1)    # 更亮的绿 -> 绿色
        curses.init_pair(COLOR_PAIRS['SKY_BLUE'], curses.COLOR_BLUE, -1)        # 天蓝 -> 蓝色
    
    return True
    
class SelectableWindow:
    def __init__(self, win, title, items):
        self.win = win
        self.title = title
        self.items = items
        self.selected_index = 0  # 当前选中的项目索引
        self.has_focus = False   # 窗口是否被选中
    def draw(self):
        # 绘制边框和标题
        border_color = curses.color_pair(2) if self.has_focus else curses.color_pair(1)
        self.win.border()
        self.win.addstr(0, 2, f" {self.title} ", border_color)
        
        # 绘制项目
        # for i, item in enumerate(self.items):
        #     # 如果项目被选中且窗口有焦点，使用选中样式
        #     if i == self.selected_index and self.has_focus:
        #         self.win.addstr(i+2, 2, f"> {item} ", curses.color_pair(2))
        #     else:
        #         self.win.addstr(i+2, 2, f"  {item} ", curses.color_pair(1))
        for i, item_dict in enumerate(self.items):
            # 获取项目文本，如果有快捷键则添加
            display_text = item_dict["text"]
            if item_dict.get("shortcut"):
                display_text = f"{display_text} ({item_dict['shortcut']})"
            
            # 如果项目被选中且窗口有焦点，使用选中样式
            if i == self.selected_index and self.has_focus:
                # 使用高亮颜色
                color_pair = item_dict.get("highlight_color", 2)  # 默认使用颜色对2
                self.win.addstr(i+2, 2, f"> {display_text} ", curses.color_pair(color_pair))
            else:
                # 使用普通颜色
                color_pair = item_dict.get("color", 1)  # 默认使用颜色对1
                self.win.addstr(i+2, 2, f"  {display_text} ", curses.color_pair(color_pair))
                # 刷新窗口
                self.win.refresh()
    
    def navigate(self, direction):
        if direction == "up":
            self.selected_index = max(0, self.selected_index - 1)
        elif direction == "down":
            self.selected_index = min(len(self.items) - 1, self.selected_index + 1)
    
    def get_selected_item(self):
        return self.items[self.selected_index]
    
def main(stdscr):
    # 初始化curses
    curses.curs_set(0)  # 隐藏光标
    stdscr.keypad(True)  # 启用特殊键模式

    # 颜色设置
    # curses.start_color()
    # curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)   # 未选中状态
    # curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)   # 选中状态
    # curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)     # 错误消息
    init_colors()
    # 创建窗口并包装成可选择的窗口对象
    
    win1 = SelectableWindow(
        curses.newwin(
            window_configs_example["time"]["size"]["height"],
            window_configs_example["time"]["size"]["width"],
            window_configs_example["time"]["size"]["y"],
            window_configs_example["time"]["size"]["x"]
        ),
    window_configs_example["time"]["title"]["text"],  # 直接传递整个 title 字典
    window_configs_example["time"]["items"]
    )
    win2 = SelectableWindow(
        curses.newwin(
            window_configs_example["attribute"]["size"]["height"],
            window_configs_example["attribute"]["size"]["width"],
            window_configs_example["attribute"]["size"]["y"],
            window_configs_example["attribute"]["size"]["x"]
        ),
    window_configs_example["attribute"]["title"]["text"],  # 直接传递整个 title 字典
    window_configs_example["attribute"]["items"]
    )
    win3 = SelectableWindow(
        curses.newwin(
            window_configs_example["class"]["size"]["height"],
            window_configs_example["class"]["size"]["width"],
            window_configs_example["class"]["size"]["y"],
            window_configs_example["class"]["size"]["x"]
        ),
    window_configs_example["class"]["title"]["text"],  # 直接传递整个 title 字典
    window_configs_example["class"]["items"]
    )
    win4 = SelectableWindow(
        curses.newwin(
            window_configs_example["action"]["size"]["height"],
            window_configs_example["action"]["size"]["width"],
            window_configs_example["action"]["size"]["y"],
            window_configs_example["action"]["size"]["x"]
        ),
    window_configs_example["action"]["title"]["text"],  # 直接传递整个 title 字典
    window_configs_example["action"]["items"]
    )
    win5 = SelectableWindow(
        curses.newwin(
            window_configs_example["echo"]["size"]["height"],
            window_configs_example["echo"]["size"]["width"],
            window_configs_example["echo"]["size"]["y"],
            window_configs_example["echo"]["size"]["x"]
        ),
    window_configs_example["echo"]["title"]["text"],  # 直接传递整个 title 字典
    window_configs_example["echo"]["items"]
    )
    win6 = SelectableWindow(
        curses.newwin(
            window_configs_example["hint"]["size"]["height"],
            window_configs_example["hint"]["size"]["width"],
            window_configs_example["hint"]["size"]["y"],
            window_configs_example["hint"]["size"]["x"]
        ),
    window_configs_example["hint"]["title"]["text"],  # 直接传递整个 title 字典
    window_configs_example["hint"]["items"]
    )
    
    windows = [win1,win2,win3,win4,win5,win6]
    active_window_idx = 0  # 当前活动窗口索引
    windows[active_window_idx].navigate("up")
    windows[active_window_idx].has_focus = True # 设置第一个窗口为活动状态
    # 初始绘制
    stdscr.clear()
    stdscr.addstr(0, 0, "使用Tab切换窗口，方向键选择项目，Enter确认，q退出", curses.color_pair(1))
    
    # 绘制所有窗口
    for win in windows:
        win.draw()
    stdscr.refresh()
    stdscr.nodelay(True)
    # 主循环
    while True:
        # 获取用户输入
        stdscr.refresh()
        key = stdscr.getch()
        # 处理键盘输入
        if key == ord('\t'):  # Tab键切换窗口
            windows[active_window_idx].has_focus = False
            active_window_idx = (active_window_idx + 1) % len(windows)
            windows[active_window_idx].has_focus = True
        elif key == curses.KEY_UP:
            windows[active_window_idx].navigate("up")
        elif key == curses.KEY_DOWN:
            windows[active_window_idx].navigate("down")
        elif key == ord('\n') or key == ord(' '):  # 回车或空格确认选择
            selected_item = windows[active_window_idx].get_selected_item()
            
            # 如果是退出选项，直接退出程序
            if selected_item == "退出":
                break
        elif key == ord('q'):
            break
        
        # 重新绘制所有窗口
        for win in windows:
            win.draw()
        
        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)