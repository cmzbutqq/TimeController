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

def list2str(lst:list)->str:
    return ', '.join(map(str,lst))

def cfg_tasks()->Table:
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
    return table

def cfg_locks()->Table:
    table = Table(title="Lock List")
    for col in ["name", "on", "punish", "list_type", "list", "time_rules"]:
        table.add_column(col)
    for lock in config.get("lockers")():
        rule_str = ''
        for rule in lock["time_rules"]:
            rule_str += f"{rule['start_time']} - {rule['end_time']} | { list2str(rule['days'])}\n"
        table.add_row(lock["name"], str(lock["on"]), lock["punish"], lock["list_type"], str(*lock["list"]), rule_str)
    return table

def cfg_presets()->Table:
    table = Table(title="Preset List")
    for col in ["key", "value"]:
        table.add_column(col)
    for k in config.keys("presets"):
        table.add_row(k, list2str(config.get("presets",k)()))
    return table

def active_timers()->Table:
    table = Table(title="Active Timers")
    
    for col in ["task id","countdown", "start", "end", "running", "used time"]:
        table.add_column(col)
    for timer in TaskTimer.instances:
        status:TimerStatus = timer.status
        cd:str= 'count up' if status.countdown is None else str(status.countdown)
        table.add_row(str(status.task_id), cd, str(status.start), str(status.end), str(status.running), str(status.used_time))
    return table

def active_lockers()->Table:
    table= Table(title="Active Lockers")
    for col in ["status","thread"]:
        table.add_column(col)
    for lockers in Locker.instances:
        table.add_row(lockers.status, str(lockers.thread))
    return table

def list_all():
    print(cfg_tasks())
    print(cfg_presets())
    print(cfg_locks())
    print(active_timers())
    print(active_lockers())

def demo_timer():
    t0=TaskTimer(0)
    t1=TaskTimer(1)
    t2=TaskTimer(2,helper.timedelta(seconds=10))
    print(active_timers())
    del t0
    t1.stop()
    print(active_timers())
    del t1
    t2.stop()
    print(active_timers())
    del t2
    print(active_timers())

def demo_locker():
    locks:list[Locker]=[Locker(idx) for idx in config.keys("lockers")]
    print(active_lockers())
    for lock in locks:lock.start()
    helper.tm.sleep(1)
    print(active_lockers())
    for lock in locks:lock.stop()
    helper.tm.sleep(1)
    print(active_lockers())
    for lock in locks:lock.start()
    helper.tm.sleep(1)
    print(active_lockers())
    for lock in locks:lock.stop()
    helper.tm.sleep(1)
    print(active_lockers())


if __name__ == '__main__':
    demo_locker()




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
