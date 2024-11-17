from services import *

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich.panel import Panel
from rich.theme import Theme
from rich.live import Live
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.spinner import Spinner
from rich.traceback import install
from rich import print,inspect
from rich import box
install()
console=Console()

command=None #主线程根据这个变量决定是否切换显示界面


def get_name(task_id:int)->str:
    for task in config.get("count_tasks")():
        if task["id"]==task_id:
            return task["name"]
    for task in config.get("timer_tasks")():
        if task["id"]==task_id:
            return task["name"]

def list2str(lst:list)->str:
    return ', '.join(map(str,lst))

def cfg_tasks()->Table:
    table = Table(title="Task List",expand=True,box=box.SIMPLE,border_style = "bright_yellow")
    for col in ["id", "name", "note", "avail", "daily", "weekly", "monthly", "deadline","type"]:
        table.add_column(col,overflow="fold")
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
    table = Table(title="Lock List",expand=True,box=box.SIMPLE,border_style = "bright_yellow")
    for col in ["name", "on", "punish", "list_type", "list", "time_rules"]:
        table.add_column(col)
    for lock in config.get("lockers")():
        rule_str = ''
        for rule in lock["time_rules"]:
            rule_str += f"{rule['start_time']} - {rule['end_time']} | { list2str(rule['days'])}\n"
        table.add_row(lock["name"], str(lock["on"]), lock["punish"], lock["list_type"], str(*lock["list"]), rule_str)
    return table

def cfg_presets()->Table:
    table = Table(title="Preset List",expand=True,box=box.SIMPLE,border_style = "bright_yellow")
    for col in ["key", "value"]:
        table.add_column(col)
    for k in config.keys("presets"):
        table.add_row(k, list2str(config.get("presets",k)()))
    return table

def active_timers()->Table:
    table = Table(title="Timer Instances",expand=True,box=box.SIMPLE,border_style = "bright_yellow")
    
    for col in ["task id","countdown", "start", "end", "running", "used time"]:
        table.add_column(col)
    for timer in TaskTimer.instances:
        status:TimerStatus = timer.status
        cd:str= 'count up' if status.countdown is None else str(status.countdown)
        table.add_row(str(status.task_id), cd, str(status.start), str(status.end), str(status.running), str(status.used_time))
    return table

def active_lockers()->Table:
    table= Table(title="Locker Instances",expand=True,box=box.SIMPLE,border_style = "bright_yellow")
    for col in ["status","thread"]:
        table.add_column(col)
    for lockers in Locker.instances:
        table.add_row(lockers.status, str(lockers.thread))
    return table

def show_cfg():
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
    )
    header=Panel(Text("CONFIGURATIONS",justify="center"),border_style="cyan")
    body=Table.grid()
    body.add_row(Panel(cfg_tasks()))
    body.add_row(Panel(cfg_locks()))
    body.add_row(Panel(cfg_presets()))
    layout["header"].update(header)
    layout["body"].update(body)
    print(layout)

def show_insts():
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
    )
    header=Panel(Text("INSTANCES",justify="center"),border_style="cyan")
    body=Table.grid()
    body.add_row(Panel(active_timers()))
    body.add_row(Panel(active_lockers()))
    layout["header"].update(header)
    layout["body"].update(body)
    print(layout)

def demo_timer():
    TaskTimer(0)
    TaskTimer(1,timedelta(seconds=2))
    TaskTimer(2,timedelta(seconds=5))
    
    print(active_timers())
    TaskTimer.run_thread()
    for _ in range(5):
        sleep(2)
        print(active_timers())
    TaskTimer.stop_thread()
    print(active_timers())
    
    TaskTimer.run_thread()
    for _ in range(2):
        sleep(1)
        print(active_timers())
    TaskTimer.stop_thread()
    print(active_timers())

locks:list[Locker]=[Locker(idx) for idx in config.keys("lockers")] 

def demo_locker():
    print(active_lockers())
    for lock in locks:lock.start()
    sleep(1)
    print(active_lockers())
    for lock in locks:lock.stop()
    sleep(1)
    print(active_lockers())
    for lock in locks:lock.start()
    sleep(1)
    print(active_lockers())
    for lock in locks:lock.stop() # 不要用 del 因为 del 能用不大可能
    sleep(1)
    print(active_lockers())

TaskTimer(3)
TaskTimer(4,timedelta(seconds=2))
TaskTimer(5,timedelta(seconds=5))
TaskTimer(6,timedelta(seconds=10))

def track_timers():
    TaskTimer.run_thread()
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
    )
    header=Panel(Text("RUNNING TIMERS",justify="center"),border_style="cyan")
    layout["header"].update(header)
    

    
    start_time = datetime.now()
    with Live(layout, refresh_per_second=100) as live:
        while datetime.now()-start_time<timedelta(seconds=15):
            body=Table.grid()
            for timer in TaskTimer.instances:
                status:TimerStatus=timer.status
                name=get_name(status.task_id)
                # if status.end is not None:
                #     continue
                grid=Table.grid()
                if status.countdown is None:
                    used=TaskRecorder.floor_dur(status.used_time)
                    speed=1 if status.running else 0
                    running = Spinner("dots",speed=speed)
                    grid.add_row(
                        Text(name+' '),
                        running,
                        Text(' '+str(used)),
                        )
                else:
                    cd=status.countdown
                    used=TaskRecorder.floor_dur(status.used_time)
                    speed=1 if status.running else 0
                    running = Spinner("dots",speed=speed)
                    percentage=round(status.used_time/status.countdown*100,1)
                    grid.add_row(
                        Text(name+' '),
                        running,
                        Text(f" {used}/{cd} - {percentage}%"),
                    )
                
                body.add_row(Panel(grid,border_style="cyan"))
                
                
                
            layout["body"].update(body)
            if datetime.now()-start_time>timedelta(seconds=14):
                TaskTimer.stop_thread()
                start_time-=timedelta(seconds=2)



track_timers()








# {
#   "lockers": [
#     {
#       "name": "控制",
#       "on": true,
#       "punish": "DEBUG",
#       "list_type": "WHITELIST",
#       "list": ["WHITE"],
#       "time_rules": [
#         {
#           "start_time": "23:10",
#           "end_time": "06:00",
#           "days": ["1-5"]
#         },
#         {
#           "start_time": "23:30",
#           "end_time": "06:00",
#           "days": ["6-7"]
#         }
#       ]
#     },
#     {
#       "name": "守护进程",
#       "on": true,
#       "punish": "DEBUG",
#       "list_type": "BLACKLIST",
#       "list": ["BLACK"],
#       "time_rules": [
#         {
#           "start_time": "23:00",
#           "end_time": "23:50",
#           "days": ["1-5"]
#         },
#         {
#           "start_time": "23:00",
#           "end_time": "23:30",
#           "days": ["6-7"]
#         }
#       ]
#     }
#   ],

#   "count_tasks": [
#     {
#       "id": 0,
#       "name": "跑步",
#       "note": "1km以上作数",
#       "activate": true,
#       "daily_aim": null,
#       "weekly_aim": 4,
#       "monthly_aim": 15,
#       "deadline_aim": { "date": "2024-12-31", "aim": 100 }
#     },
#     {
#       "id": 1,
#       "name": "跳绳",
#       "note": "累计400次作数",
#       "activate": true,
#       "daily_aim": null,
#       "weekly_aim": 4,
#       "monthly_aim": 15,
#       "deadline_aim": null
#     },
#     {
#       "id": 2,
#       "name": "完成期末论文",
#       "note": "",
#       "activate": true,
#       "daily_aim": null,
#       "weekly_aim": null,
#       "monthly_aim": null,
#       "deadline_aim": null
#     },
#     {
#       "id": 8,
#       "name": "保养自行车",
#       "note": "打气 润滑 水洗",
#       "activate": true,
#       "daily_aim": null,
#       "weekly_aim": null,
#       "monthly_aim": 1,
#       "deadline_aim": null
#     }
#   ],

#   "timer_tasks": [
#     {
#       "id": 3,
#       "name": "课上学习",
#       "note": "完成课上的作业等",
#       "activate": true,
#       "timers": ["TIMERS"],
#       "daily_aim": null,
#       "weekly_aim": 100,
#       "monthly_aim": null,
#       "deadline_aim": null
#     },
#     {
#       "id": 4,
#       "name": "自学",
#       "note": "看网课，学自己喜欢的",
#       "activate": true,
#       "timers": ["TIMERS", 80],
#       "daily_aim": null,
#       "weekly_aim": 300,
#       "monthly_aim": 1500,
#       "deadline_aim": { "date": "2024-12-31", "aim": 1000 }
#     },
#     {
#       "id": 5,
#       "name": "游戏",
#       "note": "拯救电子ED",
#       "activate": true,
#       "timers": ["TIMERS"],
#       "daily_aim": null,
#       "weekly_aim": 200,
#       "monthly_aim": null,
#       "deadline_aim": null
#     },
#     {
#       "id": 6,
#       "name": "看剧",
#       "note": "陶冶情操",
#       "activate": true,
#       "timers": ["TIMERS"],
#       "daily_aim": null,
#       "weekly_aim": 200,
#       "monthly_aim": null,
#       "deadline_aim": null
#     },
#     {
#       "id": 7,
#       "name": "弹琴",
#       "note": "优雅永不过时",
#       "activate": true,
#       "timers": ["TIMERS"],
#       "daily_aim": null,
#       "weekly_aim": 200,
#       "monthly_aim": null,
#       "deadline_aim": { "date": "2024-12-31", "aim": 1000 }
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
#   "settings": {
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

