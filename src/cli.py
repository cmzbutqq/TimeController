from services import *

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.theme import Theme
from rich.progress import track
from rich.traceback import install
from rich import print
install()
console=Console()


def list_tasks():
    table = Table(title="Task List")
    for col in ["id", "name", "note", "activate", "daily_aim", "weekly_aim", "monthly_aim", "deadline_aim","counter/timer"]:
        table.add_column(col)
    for task in config.get("count_tasks")():
        ddl=task["deadline_aim"]
        ddl=f"{ddl['aim']} times until: {ddl['date']}" if ddl is not None else "None"
        table.add_row(str(task["id"]), task["name"], task["note"], str(task["activate"]), str(task["daily_aim"]), str(task["weekly_aim"]), str(task["monthly_aim"]),ddl,'counter')
    for task in config.get("timer_tasks")():
        ddl=task["deadline_aim"]
        ddl=f"{ddl['aim']} mins until: {ddl['date']}" if ddl is not None else "None"
        table.add_row(str(task["id"]), task["name"], task["note"], str(task["activate"]), str(task["daily_aim"]), str(task["weekly_aim"]), str(task["monthly_aim"]),ddl,'timer')
    console.print(table)
        
def list_locks():
    table = Table(title="Lock List")
    for col in ["name", "on", "punish", "list_type", "list", "time_rules"]:
        table.add_column(col)
    for lock in config.get("lockers")():
        rule_str = ''
        for rule in lock["time_rules"]:
            rule_str += f"{rule['start_time']} - {rule['end_time']} | {rule['days']}\n"
        table.add_row(lock["name"], str(lock["on"]), lock["punish"], lock["list_type"], str(*lock["list"]), rule_str)
    console.print(table)

def list_presets():
    table = Table(title="Preset List")
    for col in ["name", "list"]:
        table.add_column(col)
    for preset in config.get("presets")():
        pass
    
    
list_tasks()
list_locks()
# breakpoint()

# {
#   "lockers": [
#     {
#       "name": "控制",
#       "on": false,
#       "punish": "DEBUG",
#       "list_type": "WHITELIST",
#       "list": ["WHITE"],
#       "time_rules": [
#         {
#           "start_time": "23:50",
#           "end_time": "23:51",
#           "days": ["1-5"]
#         },
#         {
#           "start_time": "00:00",
#           "end_time": "00:01",
#           "days": ["6-7"]
#         }
#       ]
#     },
#     {
#       "name": "守护进程",
#       "on": false,
#       "punish": "DEBUG",
#       "list_type": "BLACKLIST",
#       "list": ["BLACK"],
#       "time_rules": [
#         {
#           "start_time": "23:50",
#           "end_time": "23:51",
#           "days": ["1-5"]
#         },
#         {
#           "start_time": "00:00",
#           "end_time": "00:01",
#           "days": ["6-7"]
#         }
#       ]
#     }
#   ],

#   "count_tasks": [
#     {
#       "id":0,
#       "name": "运动",
#       "note": "这是计数器的备注",
#       "activate":true,
#       "daily_aim": null,
#       "weekly_aim": 4,
#       "monthly_aim": 15,
#       "deadline_aim": { "date": "2023-12-31", "aim": 100 }
#     }
#   ],

#   "timer_tasks": [
#     {
#       "id":1,
#       "name": "学习",
#       "note": "这是计时器的备注",
#       "activate":true,
#       "counters": ["TIMERS", 80],
#       "daily_aim": null,
#       "weekly_aim": 300,
#       "monthly_aim": 1500,
#       "deadline_aim": null
#     }
#   ],

#   "presets": {
#     "BLACK": ["Taskmgr.exe", "mmc.exe"],
#     "WHITE": [
#       "LockApp.exe",
#       "System Idle Process",
#       "EXCEPTION",
#       "StartMenuExperienceHost.exe",
#       "SearchHost.exe",
#       "coodesker-x64.exe",
#       "explorer.exe",
#       "QQ.exe",
#       "WeChat.exe",
#       "cloudmusic.exe"
#     ],
#     "TIMERS": [0, 5, 10, 20, 30, 45, 60],
#     "1-5": [1, 2, 3, 4, 5],
#     "6-7": [6, 7]
#   },
#   "settings":{
#     "style": {},
#     "preferences": {
#       "run_as_admin": false,
#       "auto_start": false
#     },
#     "debug": true,
#     "advanced": {
#       "lock_active_interval_sec": 1,
#       "lock_idle_interval_sec": 2,
#       "lock_off_interval_sec": 5,
#       "timer_interval_sec": 0.5
#     }
#   }
# }
